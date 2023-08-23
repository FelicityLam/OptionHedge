#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-11-25 23:23:33
LastEditTime: 2022-12-03 23:56:06
FilePath: \QTA_option_proj\src\MarketData\test_data.py
'''
import pickle
# from src.MarketData.single_stock_data import single_stock_data
# test_data = MarketData(['stock'])
# data = pd.read_csv('./data/MarketData/single_stock_data.csv', index_col=0)
# test_data.add_data('stock', '300015.SZ', data)

with open('data/MarketData/test_data.pkl', 'rb') as f:
    test_data = pickle.load(f)
    
print(test_data.asset_category)