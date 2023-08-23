# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/2 16:38
@Auth ： lizexuan
@File ：Vanilla3.py
@IDE ：PyCharm
"""

import pandas as pd
import numpy as np
from scipy import stats as st
from .BaseOption3 import BaseOption

class VanillaCall(BaseOption):
    """VanillaCall继承BaseOption类

    属性列表
    ----------
        basic_paras_df: 在基类的基础上再计算一些需要用到的参数
            - 类型: pandas.dataframe
            - index: trade_dates
            - columns: 基类的基础上再加上'd1', 'd2', 'Nd1', 'Nd2'
        greek_df: 存算的期权价格和各个希腊字母
            - 类型: pandas.dataframe
            - index: trade_dates
            - columns: 'option_price', 'delta', 'gamma', 'vega', 'theta'

    方法列表
    ----------
        calculate_vanilla_call_paras:
            计算'd1', 'd2', 'Nd1', 'Nd2'
        calculate_vanilla_call_price:
            根据BS公式的解析解计算call option价格
        calculate_vanilla_call_greeks:
            根据解析解的公式计算各个希腊字母，包括cash_greeks
    """

    def __init__(self,single_stock_data):
        super().__init__(single_stock_data)

    def calculate_vanilla_paras(self):
        self.calculate_base_paras()
        # self.basic_paras_df.loc[:, 'd1'] = (np.log(self.basic_paras_df.loc[:, 'stock_price']/self.K) + (self.r+(0.5*self.basic_paras_df.loc[:, 'sigma_2']))*self.basic_paras_df.loc[:, 'left_times'])/self.basic_paras_df.loc[:, 'sigma_T']
        self.basic_paras_df.loc[:, 'd1'] = (np.log(
            self.basic_paras_df.loc[:, 'stock_price'] / self.K) + self.r * self.basic_paras_df.loc[:,
                                                                           'left_times']) / self.basic_paras_df.loc[:,
                                                                                            'sigma_T'] + 0.5 * self.basic_paras_df.loc[
                                                                                                               :,
                                                                                                               'sigma_T']
        self.basic_paras_df.loc[:, 'd2'] = self.basic_paras_df.loc[:, 'd1'] - self.basic_paras_df.loc[:, 'sigma_T']
        self.basic_paras_df.loc[:, 'nd1'] = st.norm.pdf(self.basic_paras_df.loc[:, 'd1'])
        self.basic_paras_df.loc[:, 'Nd1'] = st.norm.cdf(self.basic_paras_df.loc[:, 'd1'])
        self.basic_paras_df.loc[:, 'Nd2'] = st.norm.cdf(self.basic_paras_df.loc[:, 'd2'])
        self.basic_paras_df.loc[:, 'Delta_S'] = self.basic_paras_df.loc[:, 'stock_price'].diff().fillna(0)
        self.basic_paras_df.loc[:, 'Delta_r'] = self.basic_paras_df.loc[:, 'Delta_S'] / self.basic_paras_df.loc[:,
                                                                                        'stock_price']

    def calculate_vanilla_price(self):
        self.calculate_vanilla_paras()
        self.greek_df = pd.DataFrame(index=self.trade_dates, columns=self.greek_columns)
        self.greek_df.loc[:, 'option_price'] = self.basic_paras_df.loc[:, 'stock_price'] * self.basic_paras_df.loc[:,
                                                                                           'Nd1'] - self.K * np.exp(
            -self.r * self.basic_paras_df.loc[:, 'left_times']) * self.basic_paras_df.loc[:, 'Nd2']
        self.greek_df.loc[:, 'stock_value'] = self.basic_paras_df.loc[:, 'stock_price'] * self.notional / self.ISP
        self.greek_df.loc[:, 'option_value'] = self.greek_df.loc[:, 'option_price'] * self.notional / self.ISP

    def calculate_vanilla_greeks(self):
        self.calculate_vanilla_price()
        self.greek_df.loc[:, 'delta'] = self.basic_paras_df.loc[:, 'Nd1']  # 看涨期权的delta是Nd1
        self.greek_df.loc[:, 'gamma'] = self.basic_paras_df.loc[:, 'nd1'] / (
                    self.basic_paras_df.loc[:, 'stock_price'] * self.basic_paras_df.loc[:, 'sigma_T'])
        self.greek_df.loc[:, 'vega'] = self.greek_df.loc[:, 'gamma'] * self.basic_paras_df.loc[:,
                                                                       'stock_price'] * self.basic_paras_df.loc[:,
                                                                                        'stock_price'] * self.basic_paras_df.loc[
                                                                                                         :, 'sigma_T']
        self.greek_df.loc[:, 'theta'] = -(self.basic_paras_df.loc[:, 'stock_price'] * self.basic_paras_df.loc[:,
                                                                                      'nd1'] * self.basic_paras_df.loc[
                                                                                               :, 'sigma'] / (
                                                      2 * np.sqrt(self.basic_paras_df.loc[:, 'left_times']))) \
                                        - self.r * self.K * np.exp(
            -self.r * self.basic_paras_df.loc[:, 'left_times']) * self.basic_paras_df.loc[:, 'Nd2']
        self.greek_df.loc[:, 'cash_delta'] = self.greek_df.loc[:, 'delta'] * self.basic_paras_df.loc[:,
                                                                             'stock_price'] * self.notional / self.ISP  # 这样不考虑股票的最小交易单位
        self.greek_df.loc[:, 'cash_gamma'] = self.greek_df.loc[:, 'gamma'] * np.power(
            self.basic_paras_df.loc[:, 'stock_price'], 2) / 100 * self.notional / self.ISP

    def get_basic_para_df(self):
        self.calculate_vanilla_paras()
        return self.basic_paras_df

    def get_greek_df(self):
        self.calculate_vanilla_greeks()
        return self.greek_df


class VanillaPut(BaseOption):
    """ 和call option方法类似，只是计算的公式不同

    gamma和vega是一样的
    """

    def __init__(self):
        super().__init__()

    def calculate_vanilla_paras(self):
        self.calculate_base_paras()
        # self.basic_paras_df.loc[:, 'd1'] = (np.log(self.basic_paras_df.loc[:, 'stock_price']/self.K) + (self.r+(0.5*self.basic_paras_df.loc[:, 'sigma_2']))*self.basic_paras_df.loc[:, 'left_times'])/self.basic_paras_df.loc[:, 'sigma_T']
        self.basic_paras_df.loc[:, 'd1'] = (np.log(
            self.basic_paras_df.loc[:, 'stock_price'] / self.K) + self.r * self.basic_paras_df.loc[:,
                                                                           'left_times']) / self.basic_paras_df.loc[:,
                                                                                            'sigma_T'] + 0.5 * self.basic_paras_df.loc[
                                                                                                               :,
                                                                                                               'sigma_T']
        self.basic_paras_df.loc[:, 'd2'] = self.basic_paras_df.loc[:, 'd1'] - self.basic_paras_df.loc[:, 'sigma_T']
        self.basic_paras_df.loc[:, 'nd1'] = st.norm.pdf(self.basic_paras_df.loc[:, 'd1'])
        self.basic_paras_df.loc[:, 'Nd1'] = st.norm.cdf(self.basic_paras_df.loc[:, 'd1'])
        self.basic_paras_df.loc[:, 'Nd2'] = st.norm.cdf(self.basic_paras_df.loc[:, 'd2'])
        self.basic_paras_df.loc[:, 'Delta_S'] = self.basic_paras_df.loc[:, 'stock_price'].diff().fillna(0)
        self.basic_paras_df.loc[:, 'Delta_r'] = self.basic_paras_df.loc[:, 'Delta_S'] / self.basic_paras_df.loc[:,
                                                                                        'stock_price']

    def calculate_vanilla_price(self):
        self.calculate_vanilla_paras()
        self.greek_df = pd.DataFrame(index=self.trade_dates, columns=self.greek_columns)
        self.greek_df.loc[:, 'option_price'] = self.basic_paras_df.loc[:, 'stock_price'] * (
                    self.basic_paras_df.loc[:, 'Nd1'] - 1) - self.K * np.exp(
            -self.r * self.basic_paras_df.loc[:, 'left_times']) * (self.basic_paras_df.loc[:, 'Nd2'] - 1)
        self.greek_df.loc[:, 'stock_value'] = self.basic_paras_df.loc[:, 'stock_price'] * self.notional / self.ISP
        self.greek_df.loc[:, 'option_value'] = self.greek_df.loc[:, 'option_price'] * self.notional / self.ISP

    def calculate_vanilla_greeks(self):
        self.calculate_vanilla_price()
        self.greek_df.loc[:, 'delta'] = self.basic_paras_df.loc[:, 'Nd1'] - 1
        self.greek_df.loc[:, 'gamma'] = self.basic_paras_df.loc[:, 'nd1'] / (
                    self.basic_paras_df.loc[:, 'stock_price'] * self.basic_paras_df.loc[:, 'sigma_T'])
        self.greek_df.loc[:, 'vega'] = self.greek_df.loc[:, 'gamma'] * self.basic_paras_df.loc[:,
                                                                       'stock_price'] * self.basic_paras_df.loc[:,
                                                                                        'stock_price'] * self.basic_paras_df.loc[
                                                                                                         :, 'sigma_T']
        self.greek_df.loc[:, 'theta'] = -(self.basic_paras_df.loc[:, 'stock_price'] * self.basic_paras_df.loc[:,
                                                                                      'nd1'] * self.basic_paras_df.loc[
                                                                                               :, 'sigma'] / (
                                                      2 * np.sqrt(self.basic_paras_df.loc[:, 'left_times']))) \
                                        + self.r * self.K * np.exp(
            -self.r * self.basic_paras_df.loc[:, 'left_times']) * self.basic_paras_df.loc[:, 'Nd2']
        self.greek_df.loc[:, 'cash_delta'] = self.greek_df.loc[:, 'delta'] * self.basic_paras_df.loc[:,
                                                                             'stock_price'] * self.notional / self.ISP  # 这样不考虑股票的最小交易单位
        self.greek_df.loc[:, 'cash_gamma'] = self.greek_df.loc[:, 'gamma'] * np.power(
            self.basic_paras_df.loc[:, 'stock_price'], 2) / 100 * self.notional / self.ISP

    def get_basic_para_df(self):
        self.calculate_vanilla_paras()
        return self.basic_paras_df

    def get_greek_df(self):
        self.calculate_vanilla_greeks()
        return self.greek_df