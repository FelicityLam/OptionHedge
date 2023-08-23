# -*- coding: utf-8 -*-
"""
@Time ： 2022/12/2 16:19
@Auth ： lizexuan
@File ：testportfolio.py
@IDE ：PyCharm
"""

from src.MarketData.MarketData import MarketData
from src.Option.BaseOption import BaseOption
from src.Option.VanillaPut import VanillaPut
from src.Option.VanillaCall import VanillaCall
from src.Option.Portfolio import OptionPortfolio

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
}
para3 = {
    'option_type': 'BullCallSpread',
    'underlying_asset': 'stock',
    'underlying_code': '300015.SZ',
    'strike_date': 20190129,
    'maturity_date': 20191231,
    'K': [27.46,28.98],
    'ISP': 27.46,
    'KS_ratio':[1,1.05],
    'strike_level':1,
    'notional': 12e6,
    'look_back_num':60,
}

option_portfolio2 = OptionPortfolio()
option_portfolio2.get_option_list(para2)
option_portfolio2.calculate_return_decomposition()
option_portfolio2.decomposition_visualize()



# single_stock_data = MarketData(['stock'])
# data = pd.read_csv('./data/MarketData/single_stock_data.csv', index_col=0)
# single_stock_data.add_data('stock', '300015.SZ', data)

# print(single_stock_data.get_data('stock', '300015.SZ'))

# para = {
#     'option_type': 'BullCallSpread',
#     'underlying_asset': 'stock',
#     'underlying_code': '300015.SZ',
#     'strike_date': 20190129,
#     'maturity_date': 20191231,
#     'K': [24.8,28.98],
#     'ISP': 24.8,
#     'KS_ratio':[1,1.16],
#     'strike_level':1,
#     'notional': 12e6,
#     'look_back_num':60,
# }
#
# option_portfolio2 = OptionPortfolio()
# option_portfolio2.get_option_list(para, single_stock_data)
# option_portfolio2.calculate_return_decomposition()
# option_portfolio2.decomposition_visualize()
#
# # paras2 = {
# #     'option_type': 'VanillaCall',
# #     'underlying_asset': 'stock',
# #     'underlying_code': '300015.SZ',
# #     'strike_date': 20190129,
# #     'maturity_date': 20191231,
# #     'K': 24.8,
# #     'ISP': 24.8,
# #     'KS_ratio':1,
# #     'strike_level':1,
# #     'notional': 12e6,
# #     'look_back_num':60,
# # }
# #
# # option_portfolio = OptionPortfolio()
# # option_portfolio.get_option_list(paras2, single_stock_data)
# # option_portfolio.calculate_return_decomposition()
# # option_portfolio.decomposition_visualize()