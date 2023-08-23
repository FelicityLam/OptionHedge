#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-11-25 22:16:05
LastEditTime: 2022-11-26 14:04:32
FilePath: \QTA_option_proj\src\MarketData\single_stock_data.py
'''
import numpy as np
import pandas as pd
from WindPy import w
import pickle
from .MarketData import MarketData
from ..tools import date_time_to_int

# def date_str_to_int(ds):
#     ds = ds.replace('/', '').replace('-', '')
#     return int(ds)

# def date_time_to_int(dt):
#     return date_str_to_int(dt.strftime('%Y%m%d'))

w.start()
w.isconnected()
codes_list = ['300015.SZ']
fields_list = ['open', 'close', 'volume', 'adjfactor', 'div_capitalization', 'div_stock']
start_date = '20170101'
end_date = '20221125'
day_type = 'Trading'
freq = 'D'
usedf = True

single_stock_data = MarketData(['stock'])
for _code in codes_list:
    err, _data = w.wsd(
            _code,
            fields_list,
            start_date,
            end_date,
            Days = day_type,
            Period = freq,
            usedf = usedf,
    )
    _data.index = map(date_time_to_int, _data.index)
    single_stock_data.data['stock'][_code] = _data

with open('data/MarketData/single_stock_data.pkl', 'wb') as f:
    pickle.dump(single_stock_data, f)

data = single_stock_data.get_data('stock','300015.SZ')
data.to_csv('data/MarketData/single_stock_data.csv')
w.stop()