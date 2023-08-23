# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/2 16:50
@Auth ： lizexuan
@File ：portfolio3.py
@IDE ：PyCharm
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .Vanilla3 import VanillaCall
from .Vanilla3 import VanillaPut
#122333444444


class OptionPortfolio():
    def __init__(self):
        self.decompose_df = pd.DataFrame(data=None,
                                         columns=['option_pnl', 'delta_pnl', 'gamma_pnl', 'theta_pnl', 'disc_pnl',
                                                  'carry_pnl', 'residual'])
        self.greek_df = pd.DataFrame(data=None)
        self.option_list = []
        self.fixbasiclist = ['sigma', 'left_days', 'left_times', 'sigma_T', 'stock_price', 'sigma_2', 'Delta_S',
                             'Delta_r']

    def get_option_list(self, para_dict, single_stock_data):
        self.option_type = para_dict.get('option_type')
        self.stock_num = para_dict.get('notional') / para_dict.get('ISP')
        self.single_stock_data = single_stock_data

        # 这里以portfolio只有一种Vanilla为例，之后需要修改初始化参数设置 暂时只用r
        # self.underlying_asse = para_dict.get('underlying_asset')
        # self.underlying_code = para_dict.get('underlying_code')
        # self.strike_date = para_dict.get('strike_date')
        # self.maturity_date = para_dict.get('maturity_date')
        # self.ISP = para_dict.get('ISP')
        # self.KS_ratio = para_dict.get('KS_ratio')
        # self.notional = para_dict.get('notional')
        # self.strike_level = para_dict.get('strike_level')
        # self.look_back_num = para_dict.get('look_back_num')
        self.r = 0.04

        if self.option_type in ['VanillaCall', 'VanillaPut']:
            option = eval(self.option_type)(self.single_stock_data)
            option.set_paras_by_dict(para_dict)
            option.calculate_vanilla_greeks()
            self.option_list.append({'option_object': option, 'option_position': 1})
        elif self.option_type == "BullCallSpread":
            option1 = VanillaCall(self.single_stock_data)
            parameter = para_dict.copy()
            parameter['K'] = min(para_dict.get('K'))
            parameter['KS_ratio'] = min(para_dict.get('KS_ratio'))
            option1.set_paras_by_dict(parameter)
            self.option_list.append({'option_object': option1, 'option_position': 1})
            option2 = VanillaCall(self.single_stock_data)
            parameter = para_dict.copy()
            parameter['K'] = max(para_dict.get('K'))
            parameter['KS_ratio'] = max(para_dict.get('KS_ratio'))
            option2.set_paras_by_dict(parameter)
            self.option_list.append({'option_object': option2, 'option_position': -1})

    def calculate_greeks(self):
        for i, element in enumerate(self.option_list):
            if i == 0:
                self.basic_paras_df = element.get('option_object').get_basic_para_df() * element.get('option_position')
                self.greek_df = element.get('option_object').get_greek_df() * element.get('option_position')
            else:
                self.basic_paras_df += element.get('option_object').get_basic_para_df() * element.get('option_position')
                self.greek_df += element.get('option_object').get_greek_df() * element.get('option_position')
        self.basic_paras_df.loc[:, self.fixbasiclist] = self.option_list[0].get('option_object').basic_paras_df.loc[:,
                                                        self.fixbasiclist]
        # print(i)
        # self.greek_df = element.get('option_object').get_greek_df()*element.get('option_position')
        # return  element.get('option_object').get_greek_df()

    def calculate_return_decomposition(self):
        self.calculate_greeks()
        self.decompose_df['option_pnl'] = self.greek_df.loc[:, 'option_value'].diff().fillna(0)
        self.decompose_df['delta_pnl'] = self.greek_df.loc[:, 'cash_delta'] * self.basic_paras_df.loc[:, 'Delta_r']
        self.decompose_df['gamma_pnl'] = 50 * self.greek_df.loc[:, 'cash_gamma'] * np.power(
            self.basic_paras_df.loc[:, 'Delta_r'], 2)
        self.decompose_df['theta_pnl'] = -50 * self.greek_df.loc[:, 'cash_gamma'] * self.basic_paras_df.loc[:,
                                                                                    'sigma_2'] * 1 / 252
        # theta_pnl = -50*cash_gamma*sigma^2*delta_t
        self.decompose_df['disc_pnl'] = self.r * self.greek_df.loc[:, 'option_value'] / 252
        self.decompose_df['carry_pnl'] = -self.greek_df.loc[:, 'cash_delta'] * self.r * 1 / 252
        self.decompose_df['residual'] = self.decompose_df.loc[:, 'option_pnl'] - self.decompose_df.loc[:,
                                                                                 'delta_pnl'] - self.decompose_df.loc[:,
                                                                                                'gamma_pnl'] \
                                        - self.decompose_df.loc[:, 'theta_pnl'] - self.decompose_df.loc[:,
                                                                                  'disc_pnl'] - self.decompose_df.loc[:,
                                                                                                'carry_pnl']

    def get_greek_df(self):
        self.calculate_greeks()
        return self.greek_df

    def get_decomposition_df(self):
        self.calculate_return_decomposition()
        return self.decompose_df

    def decomposition_visualize(self):
        df_plot = self.get_decomposition_df().copy()
        df_plot.index = np.linspace(start=0, stop=len(df_plot) / 252, num=len(df_plot))
        fig, ax1 = plt.subplots(figsize=(15, 10))
        ax1.set_xlabel('Time (Unit: year)')
        ax1.set_ylabel('Value (Unit: Yuan)')
        # ax1.invert_xaxis()
        # df_plot.loc[:, ['option_pnl','delta_pnl','gamma_pnl']].cumsum().plot(ax=ax1)
        df_plot.loc[:,
        ['option_pnl', 'delta_pnl', 'gamma_pnl', 'theta_pnl', 'disc_pnl', 'carry_pnl', 'residual']].cumsum().plot(
            ax=ax1)
        plt.show()
        # plt.plot(plot_index,df_plot['option_pnl'])
        # plt.show()
        # return plot_index