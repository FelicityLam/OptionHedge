# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/3 19:02
@Auth ： lizexuan
@File ：BaseOption.py
@IDE ：PyCharm
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from abc import abstractmethod

# 读取数据
from src.MarketData.MarketData import MarketData
from ..MarketData.test_data import test_data as market_data

# single_stock_data = MarketData(['stock'])
# data = pd.read_csv('./data/MarketData/single_stock_data.csv', index_col=0)
# single_stock_data.add_data('stock', '300015.SZ', data)
# 读取数据

class BaseOption:
    """期权基类

    所有方法列表
    ----------
        reset_paras:
            初始化参数设置，都设置为none，look_back_num设置为10个交易日
        set_paras_by_dict:
            根据传入的字典初始化合约级参数设置
        calculate_base_paras:
            计算与期限相关的参数，运行以下四个方法
        calculate_trade_dates:
            设置trade_dates和look_back_dates
        get_spot_price:
            读取保存look_back_dates时间段内的股价数据
        calculate_vols:
            计算trade_dates窗口期内的vol
        calculate_basic_paras:
            计算basic_paras_df里'sigma', 'left_days', 'left_times', 'sigma_T', 'delta_s', 'delta_r'
        pnl_decomposition:
            计算option端的pnl拆解，传入greeks，计算好各个pnl保存在decompose_df中

    """

    greek_columns = ['delta', 'gamma', 'vega', 'theta', 'option_price']
    underlying_asset_base_type = ['stock', 'index_futures']
    basic_paras_columns = ['sigma', 'left_days', 'left_times', 'sigma_T', 'stock_price']

    def __init__(self):  # 合约级的参数需要初始化输入，随着交易日时变的参数后面再计算
        self.reset_paras()

    def reset_paras(self):
        self.underlying_asset = None
        self.underlying_code = None
        self.strike_date = None
        self.maturity_date = None
        self.ISP = None
        self.KS_ratio = 1
        self.notional = 0
        self.strike_level = 0
        self.look_back_num = 10
        self.r = 0.04
        self.option_position = 1
        self.greek_df: pd.DataFrame = None

    def set_paras(self, underlying_asset=None, underlying_code=None, strike_date=None,
                  maturity_date=None, ISP=None, option_position=None, KS_ratio=1, strike_level=0):
        self.underlying_asset = underlying_asset
        self.underlying_code = underlying_code
        self.strike_date = strike_date
        self.maturity_date = maturity_date
        self.ISP = ISP
        self.KS_ratio = KS_ratio
        self.option_position = option_position
        self.notional = 0
        self.strike_level = strike_level
        self.look_back_num = 10
        self.set_all_trade_dates()

    def set_paras_by_dict(self, para_dict):
        self.parameters = para_dict
        self.set_basic_paras(para_dict)

    def set_basic_paras(self, para_dict):
        """通过字典输入初始化参数
        date, ISP, KS_ratio,  look_back_num
        传入合约级别的不随时间变化的参数设置
        """
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

    def set_all_trade_dates(self):
        self.all_trade_dates = market_data.get_data(self.underlying_asset, self.underlying_code).index.tolist()
        
    def set_notional(self, notional=None):
        if notional is not None:
            self.notional = notional

    def set_underlying_asset(self, underlying_asset_input=None):
        if underlying_asset_input in self.underlying_asset_base_type:
            self.underlying_asset = underlying_asset_input
        else:
            raise ValueError('Invalid underlying_asset!')

    def set_underlying_code(self, underlying_code=None):
        if underlying_code is not None:
            self.underlying_code = underlying_code

    def set_strike_date(self, strike_date=None):
        if strike_date is not None:
            self.strike_date = strike_date

    def set_maturity_date(self, maturity_date=None):
        if maturity_date is not None:
            self.maturity_date = maturity_date

    def set_ISP(self, ISP=None):
        if ISP is not None:
            self.ISP = ISP

    def set_KS_ratio(self, KS_ratio=1):
        if KS_ratio is not None:
            self.KS_ratio = KS_ratio

    def set_K(self):
        self.K = self.KS_ratio * self.ISP

    def set_strike_level(self, strike_level=0):
        if strike_level is not None:
            self.strike_level = strike_level

    def set_look_back_num(self, look_back_num=10):
        if look_back_num is not None:
            self.look_back_num = look_back_num

    def set_option_position(self, option_position=10):
        if option_position is not None:
            self.option_position = option_position

    def calculate_base_paras(self):
        self.calculate_trade_dates()
        self.get_spot_prices()
        self.calculate_vols()
        self.calculate_basic_paras()

    def calculate_trade_dates(self):
        """计算起息日到期日和要用于计算vol的时间窗口

        trade_dates时间段为起息日到到期日，look_back_dates为trade_dates再加上往前look_back_num个交易日的时间窗口
        """
        self.start_idx = self.all_trade_dates.index(self.strike_date)
        self.end_idx = self.all_trade_dates.index(self.maturity_date) + 1
        self.trade_dates = self.all_trade_dates[self.start_idx:self.end_idx]
        self.look_back_date = self.all_trade_dates[self.start_idx - self.look_back_num]
        self.look_back_dates = self.all_trade_dates[self.start_idx - self.look_back_num:self.end_idx]
        self.trade_dates_length = len(self.trade_dates)

    def get_spot_prices(self):
        """提取look_bakck_dates内的股票价格

        从single_stock_data里提取对应股票代码的CLOSE列收盘价，spot_price是look_back_dates内的收盘价
        """
        if self.underlying_code is None:
            print('标的资产代码未设定')
            return -1
        self.spot_price = market_data.get_data(self.underlying_asset, self.underlying_code).loc[self.look_back_dates, 'CLOSE']
        # 加上折现因子
        # self.spot_price = single_stock_data.get_data('stock', '300015.SZ').loc[self.look_back_dates, 'CLOSE']\
        #     *single_stock_data.get_data('stock', '300015.SZ').loc[self.look_back_dates, 'ADJFACTOR']

    def calculate_vols(self):
        """根据look_back_dates内的股票价格计算trade_dates内的vol

        用历史波动率表示隐含波动率
        """
        self.percent_change = self.spot_price.pct_change()
        # 移动窗口的长度是look_back_num的长度，计算std
        self.volatility = self.percent_change.rolling(self.look_back_num).std()[self.look_back_num:] * np.sqrt(252)  

    def calculate_basic_paras(self):
        """计算sigma，期限以及年化的剩余期限

        sigma = volatility,用历史波动率代替隐含波动率
        left_days计算还有多少个交易日到期
        left_times计算年化的left_days
        sigma_T = sigma * sqrt(left_times) 对应用于之后BS公式计算
        """
        self.basic_paras_df = pd.DataFrame(data=None, columns=self.basic_paras_columns)
        self.basic_paras_df.loc[:, 'sigma'] = self.volatility.dropna()
        self.basic_paras_df.loc[:, 'sigma_2'] = self.basic_paras_df.loc[:, 'sigma'] * self.basic_paras_df.loc[:,
                                                                                      'sigma']
        self.basic_paras_df.loc[:, 'left_days'] = np.linspace(self.trade_dates_length - 1, 0, self.trade_dates_length)
        self.basic_paras_df.loc[:, 'left_times'] = self.basic_paras_df.loc[:, 'left_days'] / 252
        self.basic_paras_df.loc[:, 'sigma_T'] = self.basic_paras_df.loc[:, 'sigma'] * np.sqrt(
            self.basic_paras_df.loc[:, 'left_times'])
        self.basic_paras_df.loc[:, 'stock_price'] = self.spot_price.loc[self.trade_dates]
        self.basic_paras_df.loc[:, 'Delta_S'] = self.basic_paras_df.loc[:, 'stock_price'].diff().fillna(0)
        self.basic_paras_df.loc[:, 'Delta_r'] = self.basic_paras_df.loc[:, 'Delta_S'] / self.basic_paras_df.loc[:,
                                                                                        'stock_price']

    @abstractmethod
    def calculate_option_paras(self):
        """计算一些其他的参数，比如VanillaOption里面的d1，d2等等
        """
        pass
    
    @abstractmethod
    def calculate_option_greeks(self):
        """计算期权对应的希腊字母
        """
        pass

    def pnl_decompose(self, greek_df):
        self.decompose_df = pd.DataFrame(data=None,
                                         columns=['option_pnl', 'delta_pnl', 'gamma_pnl', 'theta_pnl', 'disc_pnl',
                                                  'carry_pnl', 'residual'])
        self.decompose_df['option_pnl'] = greek_df.loc[:, 'option_value'].diff().fillna(0)
        self.decompose_df['delta_pnl'] = greek_df.loc[:, 'cash_delta'] * self.basic_paras_df.loc[:, 'Delta_r']
        self.decompose_df['gamma_pnl'] = 50 * greek_df.loc[:, 'cash_gamma'] * np.power(
            self.basic_paras_df.loc[:, 'Delta_r'], 2)
        self.decompose_df['theta_pnl'] = -50 * greek_df.loc[:, 'cash_gamma'] * self.basic_paras_df.loc[:,
                                                                               'sigma_2'] * 1 / 252
        self.decompose_df['disc_pnl'] = self.r * greek_df.loc[:, 'option_value'] / 252
        self.decompose_df['carry_pnl'] = -greek_df.loc[:, 'cash_delta'] * self.r * 1 / 252
        self.decompose_df['residual'] = self.decompose_df.loc[:, 'option_pnl'] - self.decompose_df.loc[:,
                                                                                 'delta_pnl'] - self.decompose_df.loc[:,
                                                                                                'gamma_pnl'] \
                                        - self.decompose_df.loc[:, 'theta_pnl'] - self.decompose_df.loc[:,
                                                                                  'disc_pnl'] - self.decompose_df.loc[:,
                                                                                                'carry_pnl']
        return self.decompose_df
    
    def decomposition_visualize(self, decompose_df):
        df_plot = decompose_df.copy()
        df_plot.index = np.linspace(start=0, stop=len(df_plot) / 252, num=len(df_plot))
        fig, ax1 = plt.subplots(figsize=(15, 10))
        ax1.set_xlabel('Time (Unit: year)')
        ax1.set_ylabel('Value (Unit: Yuan)')
        df_plot.loc[:,
        ['option_pnl', 'delta_pnl', 'gamma_pnl', 'theta_pnl', 'disc_pnl', 'carry_pnl', 'residual']].cumsum().plot(
            ax=ax1)
        plt.show()