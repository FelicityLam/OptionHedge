#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-11-26 14:22:58
LastEditTime: 2022-12-02 13:51:01
FilePath: \QTA_option_proj\src\Option\BaseOption.py
'''
import pandas as pd
from abc import abstractmethod

class BaseOption():
    
    def __init__(self):
        self.underlying_asset: str
        self.underlying_code: str
        self.strike_date: int
        self.maturity: int
        self.ISP: float
        self.KSratio: float
        self.strike_level: int # -1 0 1: OTM, ATM, ITM
        self.greeks: pd.DataFrame
        self.bs_params: pd.DataFrame
    
    @abstractmethod
    def cal_BS_params():
        pass
    
    @abstractmethod
    def cal_greeks():
        pass
    
    @abstractmethod
    def pnl_decompose():
        pass