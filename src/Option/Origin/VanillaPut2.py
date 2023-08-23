import numpy as np
from src.Option.Origin.BaseOption import BaseOption


class VanillaPut(BaseOption):
    
    def __init__(self):
        super().__init__()
    
    def set_strike_level(self):
        if self.KSratio is not None:
            if self.KSratio < 1:
                self.strike_level = 1
            elif self.KSratio == 1:
                self.strike_level = 0
            else:
                self.strike_level = -1
                
    def cal_BS_params(self):
        super().cal_BS_params()
        self.BS_params['p'] = self.KSratio*self.ISP*np.exp(-self.r*self.BS_params['remain_period'])*(1-self.BS_params['Nd2'])-self.BS_params['close']*(1-self.BS_params['Nd1'])
    
    def cal_greeks(self):
        self.greeks['delta'] = self.BS_params['Nd1'] - 1
        self.greeks['gamma'] = np.exp(-self.BS_params['d1']**2/2)/(self.BS_params['close']*self.BS_params['sigma']*np.sqrt(2*np.pi*self.BS_params['remain_period']))
        self.greeks['theta'] = -(self.BS_params['sigma']*self.BS_params['close']*np.exp(-self.BS_params['d1']**2/2))/(2*np.sqrt(2*np.pi**2*self.BS_params['remain_period']))+self.r*self.KSratio*self.ISP*np.exp(-self.r*self.BS_params['remain_period'])*(1-self.BS_params['Nd2'])
        self.greeks['vega'] = (self.BS_params['close']*np.sqrt(self.BS_params['remain_period']))/np.sqrt(2*np.pi)*np.exp(-self.BS_params['d1']**2/2)

