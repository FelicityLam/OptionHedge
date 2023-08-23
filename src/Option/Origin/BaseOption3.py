# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/2 16:12
@Auth ： lizexuan
@File ：BaseOption3.py
@IDE ：PyCharm
"""
import pandas as pd
import numpy as np
from src.MarketData.MarketData import MarketData
# from ..MarketData.single_stock_data import single_stock_data

class BaseOption:
    """期权基类

    所有属性列表
    ----------
        underlying_asset_base_type: 对应MarketData里面的asset_category
            - 类型: list
            - 值: 'stock','index_futures'
        underlying_asset: 标的类型
            - 类型: str
        underlying_code: 标的代码
            - 类型: str
        strike_date: 起息日
            - 类型: str
        maturity_date: 到期日
            - 类型: str
        ISP: initial spot price
            - 类型: float
        KS_ratio: K/S
            - 类型: float
        K: 执行价格 = KS_ratio*ISP
            - 类型: float
        r: 无风险利率 默认设置为0.04
            - 类型: float
        strike_level: 根据KSratio判定 OTM, ATM, ITM
            - 类型: int
        look_back_num: 用多长时间窗口内的股价来计算vol，默认60个交易日
            - 类型: int
        all_trade_dates: 记录股价数据中所有的交易日
            - 类型: list
        trade_dates: 起息日到到期日
            - 类型: list
        start_idx: 起息日在所有交易日中是第几天
            - 类型: int
        end_idx: 到期日在所有交易日中是第几天
            - 类型: int
        look_back_dates: trade_date加上算vol的一小段时间窗口的时间
            - 类型: list
        stock_prices: 对应标的在look_back_dates内每天的股价
            - 类型: pandas.Series
            - index: look_back_dates
        volatility: 对应标的在look_back_dates内窗口期内的vol
            - 类型: pandas.Series
            - index: trade_dates
        basic_paras_df: 按照每个交易日计算得到的时变参数信息
            - 类型: pandas.dataframe
            - index: trade_dates
            - columns: 'sigma', 'left_days', 'left_times', 'sigma_T', 'stock_price'

    所有方法列表
    ----------
        reset_paras:
            初始化参数设置，都设置为none，look_back_num设置为10个交易日
        set_paras_by_dict:
            根据传入的字典初始化合约级参数设置
        calculate_base_paras:
            计算与期限相关的参数，运行以下所有方法
        calculate_trade_dates:
            设置trade_dates和look_back_dates
        get_stock_prices:
            读取保存look_back_dates时间段内的股价数据
        calculate_vols:
            计算trade_dates窗口期内的vol
        calculate_basic_paras:
            计算basic_paras_df里'sigma', 'left_days', 'left_times', 'sigma_T'

    """

    greek_columns = ['delta', 'gamma', 'vega', 'theta', 'option_price']
    underlying_asset_base_type = ['stock', 'index_futures']
    basic_paras_columns = ['sigma', 'left_days', 'left_times', 'sigma_T', 'stock_price']

    def __init__(self,single_stock_data):  # 合约级的参数需要初始化输入，随着交易日时变的参数后面再计算
        self.reset_paras()
        self.single_stock_data = single_stock_data
        self.all_trade_dates = self.single_stock_data.get_data('stock', '300015.SZ').index.tolist()
        # self.greek_df = pd.DataFrame(data=None, columns= self.greek_columns)

    def receive(self,single_stock_data):
        self.single_stock_data = single_stock_data

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

    def set_paras(self, underlying_asset=None, underlying_code=None, strike_date=None,
                  maturity_date=None, ISP=None, KS_ratio=1, strike_level=0):
        self.underlying_asset = underlying_asset
        self.underlying_code = underlying_code
        self.strike_date = strike_date
        self.maturity_date = maturity_date
        self.ISP = ISP
        self.KS_ratio = KS_ratio
        self.notional = 0
        self.strike_level = strike_level
        self.look_back_num = 10

    def set_paras_by_dict(self, para_dict):
        self.parameters = para_dict
        self.set_basic_paras(para_dict)

    def set_basic_paras(self, para_dict):
        """通过字典输入初始化参数
        date, ISP, KS_ratio, notional, look_back_num
        传入合约级别的不随时间变化的参数设置
        """
        self.set_underlying_asset(para_dict.get('underlying_asset'))
        self.set_underlying_code(para_dict.get('underlying_code'))
        self.set_strike_date(para_dict.get('strike_date'))
        self.set_maturity_date(para_dict.get('maturity_date'))
        self.set_ISP(para_dict.get('ISP'))
        self.set_KS_ratio(para_dict.get('KS_ratio'))
        self.set_notional(para_dict.get('notional'))
        self.set_strike_level(para_dict.get('strike_level'))
        self.set_look_back_num(para_dict.get('look_back_num'))
        self.set_K()

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

    def calculate_base_paras(self):
        self.calculate_trade_dates()
        self.get_stock_prices()
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

    def get_stock_prices(self):
        """提取look_bakck_dates内的股票价格

        从single_stock_data里提取对应股票代码的CLOSE列收盘价，stock_prices是look_back_dates内的收盘价
        """
        if self.underlying_code is None:
            print('标的资产代码未设定')
            return -1
        self.stock_prices = self.single_stock_data.get_data('stock', '300015.SZ').loc[self.look_back_dates, 'CLOSE']
        # BasicData.basicData['close'].loc[self.look_back_dates, self.underlying_code]

    def calculate_vols(self):
        """根据look_back_dates内的股票价格计算trade_dates内的vol

        用历史波动率表示隐含波动率
        """
        self.percent_change = self.stock_prices.pct_change()
        self.volatility = self.percent_change.rolling(self.look_back_num).std()[self.look_back_num:] * np.sqrt(
            252)  # 移动窗口的长度是look_back_num的长度，计算std

    def calculate_basic_paras(self):
        """计算sigma，期限以及年化的剩余期限

        sigma = volatility,用历史波动率代替隐含波动率
        left_days计算还有多少个交易日到期
        left_times计算年化的left_days
        sigma_T = sigma * sqrt(left_times) 对应用于之后BS公式计算
        """
        #     self.get_stock_prices()
        #     self.calculate_vols()
        self.basic_paras_df = pd.DataFrame(data=None, columns=self.basic_paras_columns)
        self.basic_paras_df.loc[:, 'sigma'] = self.volatility.dropna()
        self.basic_paras_df.loc[:, 'sigma_2'] = self.basic_paras_df.loc[:, 'sigma'] * self.basic_paras_df.loc[:,
                                                                                      'sigma']
        self.basic_paras_df.loc[:, 'left_days'] = np.linspace(self.trade_dates_length - 1, 0, self.trade_dates_length)
        self.basic_paras_df.loc[:, 'left_times'] = self.basic_paras_df.loc[:, 'left_days'] / 252
        self.basic_paras_df.loc[:, 'sigma_T'] = self.basic_paras_df.loc[:, 'sigma'] * np.sqrt(
            self.basic_paras_df.loc[:, 'left_times'])
        self.basic_paras_df.loc[:, 'stock_price'] = self.stock_prices.loc[self.trade_dates]
