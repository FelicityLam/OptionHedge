#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-11-25 23:23:33
LastEditTime: 2022-11-26 14:10:40
FilePath: \QTA_option_proj\test_data.py
'''
from src.MarketData.MarketData import MarketData
import pandas as pd
# from src.MarketData.single_stock_data import single_stock_data

single_stock_data = MarketData(['stock'])
data = pd.read_csv('./data/MarketData/single_stock_data.csv', index_col=0)

single_stock_data.add_data('stock', '300015.SZ', data)

print(single_stock_data)
print(single_stock_data.get_data('stock', '300015.SZ'))