import pandas as pd
import numpy as np
from scipy import stats as st
from abc import abstractmethod
from src.MarketData.single_stock_data import single_stock_data


class BaseOption:
    """
    属性列表
    -------
        underlying_asset：标的资产类型
            - 类型：str
            - 值：'stock', 'index_futures'
        underlying_code：标的资产代码
            - 类型：str
            - 值：'300015.SZ'
        strike_date：起息日
            - 类型：int
        maturity：到期日
            - 类型：int
        ISP：Initial Spot Price
            - 类型：float
        KSratio：strike / ISP
            - 类型：float
        strike_level：OTM/ATM/ITM
            - 类型：int
            - 值：-1, 0, 1
        greeks：希腊字母值
            - 类型：pd.DataFrame
            - 值：index为trade_dates，columns为['CLOSE', 'delta', 'gamma', 'theta', 'vega']
        BS_params：BS公式参数
            - 类型：pd.DataFrame
            - 值：index为trade_dates，columns为['d1', 'd2', 'Nd1', 'Nd2']
        sigma_period：计算历史波动率向前rolling的天数
            - 类型：int
            - 值：60
        r：无风险利率
            - 类型：float
            - 值：0.04
        all_trade_dates：所有交易日
            - 类型：list
        trade_dates：起息日到到期日
            - 类型：list
        look_back_dates：trade_dates向前sigma_period个交易日
            - 类型：list
    """
    def __init__(self):
        self.reset_params()
        self.all_trade_dates = single_stock_data.get_data('stock', '300015.SZ').index.tolist()
        
    def reset_params(self):
        self.underlying_asset = None
        self.underlying_code = None
        self.strike_date = None
        self.maturity = None
        self.ISP = None
        self.Ktrike_level = None
        self.greeks = NoneSratio = None
        self.s
        self.BS_params = None
        self.sigma_period = 60
        self.r = 0.04
        
    def set_params(
        self, 
        underlying_asset=None, 
        underlying_code=None, 
        strike_date=None,
        maturity=None,
        ISP=None,
        KSratio=None,
        sigma_period=None,
        r=None
    ):
        self.set_underlying_asset(underlying_asset)
        self.set_underlying_code(underlying_code)
        self.set_strike_date(strike_date)
        self.set_maturity(maturity)
        self.set_ISP(ISP)
        self.set_KSratio(KSratio)
        self.set_strike_level()
        self.set_sigma_period(sigma_period)
        self.set_r(r)
    
    def set_underlying_asset(self, underlying_asset=None):
        if underlying_asset is not None:
            self.underlying_asset = underlying_asset
    
    def set_underlying_code(self, underlying_code=None):
        if underlying_code is not None:
            self.underlying_code = underlying_code
    
    def set_strike_date(self, strike_date=None):
        if strike_date is not None:
            self.strike_date = strike_date
    
    def set_maturity(self, maturity=None):
        if maturity is not None:
            self.maturity = maturity
            
    def set_ISP(self, ISP=None):
        if ISP is not None:
            self.ISP = ISP
    
    def set_KSratio(self, KSratio=None):
        if KSratio is not None:
            self.KSratio = KSratio

    @abstractmethod
    def set_strike_level(self):
        pass
    
    def set_sigma_period(self, sigma_period):
        if sigma_period is not None:
            self.sigma_period = sigma_period

    def set_r(self, r):
        if r is not None:
            self.r = r

    def get_trade_dates(self):
        strike_idx = self.all_trade_dates.index(self.strike_date)
        maturity_idx = self.all_trade_dates.index(self.maturity)
        self.trade_dates = self.all_trade_dates[strike_idx:maturity_idx+1]
        self.look_back_dates = self.all_trade_dates[strike_idx-self.sigma_period:maturity_idx+1]

    def get_stock_data(self):
        if self.underlying_code is None:
            print('股票代码未设定')
            return -1
        self.get_trade_dates()
        self.BS_params = single_stock_data.get_data('stock', '300015.SZ').loc[self.look_back_dates, 'CLOSE']
        # self.BS_params = single_stock_data.get_data(self.underlying_asset, underlying_code).loc[self.look_back_dates,

    def cal_volatility(self):
        self.get_stock_data()
        vol = self.BS_params['CLOSE'].pct_change().rolling(self.sigma_period).std() * np.sqrt(252)
        self.BS_params['sigma'] = vol.dropna()

    # call price and put price will be extended in VanillaCall and VanillaPut
    def cal_BS_params(self):
        self.get_stock_data()
        self.BS_params['remain_period'] = np.linspace(len(self.BS_params)-1, 0.0001, len(self.BS_params)) / 252
        self.BS_params['d1'] = (np.log(self.BS_params['close']/(self.KSratio*self.ISP))+(self.r+self.BS_params['sigma']**2/2)*self.BS_params['remain_period'])/(self.BS_params['sigma']*np.sqrt(self.BS_params['remain_period']))
        self.BS_params['d2'] = self.BS_params['d1'] - self.BS_params['sigma'] * np.sqrt(self.BS_params['remain_period'])
        self.BS_params['Nd1'] = st.norm.cdf(self.BS_params['d1'])
        self.BS_params['Nd2'] = st.norm.cdf(self.BS_params['d2'])
    
    @abstractmethod
    def cal_greeks(self):
        pass

