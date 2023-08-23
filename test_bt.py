#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-12-03 23:23:03
LastEditTime: 2022-12-04 00:19:53
FilePath: \QTA_option_proj\test_bt.py
'''
from src.BackTest.Backtest import Backtest
from src.Strategy.HedgeAllStrategy import HedgeAllStrategy
from src.Option.Portfolio import OptionPortfolio
import warnings
warnings.filterwarnings('ignore')
para2 = {
    'option_type': 'VanillaCall',
    'underlying_asset': 'stock',
    'underlying_code': '300015.SZ',
    'strike_date': 20190129,
    'maturity_date': 20191231,
    'K': 27.46,
    'ISP': 27.46,
    'KS_ratio':1,
    'strike_level':1,
    'notional': 12e6,
    'look_back_num':60,
    'option_position':10,
}

option_portfolio = OptionPortfolio()
option_portfolio.get_option_list(para2)
option_portfolio.pnl_decompose()
option_portfolio.decomposition_visualize()

hedge_all_strategy = HedgeAllStrategy(option_portfolio, hedge_asset='stock', hedge_code=['300015.SZ'])
hedge_all_strategy.pnl_decompose()

bt = Backtest(hedge_all_strategy, option_portfolio)
bt.report(to_save_dir='./res/')
print('end')
