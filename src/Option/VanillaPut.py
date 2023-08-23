#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-12-03 22:28:19
LastEditTime: 2022-12-04 00:00:29
FilePath: \QTA_option_proj\src\Option\VanillaPut.py
'''
# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/3 19:23
@Auth ： lizexuan
@File ：VanillaPut.py
@IDE ：PyCharm
"""

import pandas as pd
import numpy as np
from scipy import stats as st
from .BaseOption import BaseOption


class VanillaPut(BaseOption):
    """ 和call option方法类似，只是计算的公式不同

    gamma和vega是一样的
    """

    def __init__(self):
        super().__init__()

    def set_paras_by_dict(self, para_dict):
        super().set_paras_by_dict(para_dict)
        self.set_notional(para_dict.get('notional'))

    def calculate_option_paras(self):
        self.calculate_base_paras()
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

    def calculate_option_price(self):
        self.calculate_option_paras()
        self.greek_df = pd.DataFrame(index=self.trade_dates, columns=self.greek_columns)
        self.greek_df.loc[:, 'option_price'] = self.basic_paras_df.loc[:, 'stock_price'] * (
                    self.basic_paras_df.loc[:, 'Nd1'] - 1) - self.K * np.exp(
            -self.r * self.basic_paras_df.loc[:, 'left_times']) * (self.basic_paras_df.loc[:, 'Nd2'] - 1)
        self.greek_df.loc[:, 'stock_value'] = self.basic_paras_df.loc[:, 'stock_price'] * self.notional / self.ISP
        self.greek_df.loc[:, 'option_value'] = self.greek_df.loc[:, 'option_price'] * self.notional / self.ISP * self.option_position

    def calculate_option_greeks(self):
        self.calculate_option_price()
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
        # self.greek_df.loc[:,'cash_delta'] = self.greek_df.loc[:,'delta']*self.basic_paras_df.loc[:,'stock_price']*self.notional/self.ISP    #这样不考虑股票的最小交易单位
        self.greek_df.loc[:, 'cash_delta'] = self.greek_df.loc[:, 'delta'] * self.notional * self.option_position # 这样不考虑股票的最小交易单位
        self.greek_df.loc[:, 'cash_gamma'] = self.greek_df.loc[:, 'gamma'] * self.notional * self.basic_paras_df.loc[:,
                                                                                             'stock_price'] / 100 * self.option_position

    def get_basic_para_df(self):
        self.calculate_option_paras()
        return self.basic_paras_df

    def get_greek_df(self):
        self.calculate_option_greeks()
        return self.greek_df

    def get_pnl_decompose_df(self):
        self.calculate_option_greeks()
        self.pnl_decompose(self.greek_df)
        return self.decompose_df
