#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-12-03 22:28:19
LastEditTime: 2022-12-03 23:58:06
FilePath: \QTA_option_proj\src\Option\Portfolio.py
'''
# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/3 19:29
@Auth ： lizexuan
@File ：Portfolio.py
@IDE ：PyCharm
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .VanillaCall import VanillaCall
from .VanillaPut import VanillaPut
from .BaseOption import BaseOption


class OptionPortfolio(BaseOption):
    """
    portfolio在get_option_list()里初始化期权合约级参数
    关于日期的属性：
        all_trade_dates: 记录股价数据中所有的交易日
            - 类型: list
        trade_dates: 起息日到到期日
            - 类型: list
        look_back_dates: trade_date加上算vol的一小段时间窗口的时间
            - 类型: list
    返回greeks和日期的方法：
        get_decomposition_df: 返回self.decompose_df，index是trade_dates，columns是pnl
        get_trade_date: 返回self.trade_dates
    """
    def __init__(self):
        self.decompose_df = pd.DataFrame(data=None,
                                         columns=['option_pnl', 'delta_pnl', 'gamma_pnl', 'theta_pnl', 'disc_pnl',
                                                  'carry_pnl', 'residual'])
        self.greek_df = pd.DataFrame(data=None)
        self.option_list = []
        self.fixbasiclist = ['sigma', 'left_days', 'left_times', 'sigma_T', 'stock_price', 'sigma_2', 'Delta_S',
                             'Delta_r']

    def get_option_list(self, para_dict):
        self.option_type = para_dict.get('option_type')
        self.stock_num = para_dict.get('notional') / para_dict.get('ISP')

        #初始化portfolio的合约级参数，这里以portfolio只有一种Vanilla为例
        self.set_underlying_asset(para_dict.get('underlying_asset'))
        self.set_underlying_code(para_dict.get('underlying_code'))
        self.set_strike_date(para_dict.get('strike_date'))
        self.set_maturity_date(para_dict.get('maturity_date'))
        self.set_ISP(para_dict.get('ISP'))
        self.set_KS_ratio(para_dict.get('KS_ratio'))
        # self.set_notional(para_dict.get('notional'))
        self.set_strike_level(para_dict.get('strike_level'))
        self.set_look_back_num(para_dict.get('look_back_num'))
        self.set_option_position(para_dict.get('option_position'))
        self.set_K()
        self.set_all_trade_dates()

        if self.option_type in ['VanillaCall', 'VanillaPut']:
            option = eval(self.option_type)()
            option.set_paras_by_dict(para_dict)
            option.calculate_option_greeks()
            self.option_list.append({'option_object': option, 'option_position': 1})
        elif self.option_type == "BullCallSpread":
            option1 = VanillaCall()
            parameter = para_dict.copy()
            parameter['K'] = min(para_dict.get('K'))
            parameter['KS_ratio'] = min(para_dict.get('KS_ratio'))
            option1.set_paras_by_dict(parameter)
            self.option_list.append({'option_object': option1, 'option_position': 1})
            option2 = VanillaCall()
            parameter = para_dict.copy()
            parameter['K'] = max(para_dict.get('K'))
            parameter['KS_ratio'] = max(para_dict.get('KS_ratio'))
            option2.set_paras_by_dict(parameter)
            self.option_list.append({'option_object': option2, 'option_position': -1})

    def calculate_option_greeks(self):
        for i, element in enumerate(self.option_list):
            if i == 0:
                self.basic_paras_df = element.get('option_object').get_basic_para_df() * element.get('option_position')
                self.greek_df = element.get('option_object').get_greek_df() * element.get('option_position')
            else:
                self.basic_paras_df += element.get('option_object').get_basic_para_df() * element.get('option_position')
                self.greek_df += element.get('option_object').get_greek_df() * element.get('option_position')
        self.basic_paras_df.loc[:, self.fixbasiclist] = self.option_list[0].get('option_object').basic_paras_df.loc[:,
                                                        self.fixbasiclist]

    def pnl_decompose(self):
        self.calculate_option_greeks()
        for i, element in enumerate(self.option_list):
            if i == 0:
                self.decompose_df = element.get('option_object').get_pnl_decompose_df() * element.get('option_position')
            else:
                self.decompose_df += element.get('option_object').get_pnl_decompose_df() * element.get(
                    'option_position')

    def get_trade_dates(self):
        self.calculate_trade_dates()
        return self.trade_dates

    def get_greek_df(self):
        self.calculate_option_greeks()
        return self.greek_df

    def get_decomposition_df(self):
        self.pnl_decompose()
        return self.decompose_df

    def decomposition_visualize(self):
        df_plot = self.get_decomposition_df().copy()
        df_plot.index = np.linspace(start=0, stop=len(df_plot) / 252, num=len(df_plot))
        fig, ax1 = plt.subplots(figsize=(15, 10))
        ax1.set_xlabel('Time (Unit: year)')
        ax1.set_ylabel('Value (Unit: Yuan)')
        df_plot.loc[:,
        ['option_pnl', 'delta_pnl', 'gamma_pnl', 'theta_pnl', 'disc_pnl', 'carry_pnl', 'residual']].cumsum().plot(
            ax=ax1)
        plt.show()