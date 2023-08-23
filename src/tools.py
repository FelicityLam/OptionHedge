#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-11-25 23:12:10
LastEditTime: 2022-11-26 22:27:56
FilePath: \QTA_option_proj\src\tools.py
'''
import pandas as pd
import datetime

def date_str_to_int(ds):
    ds = ds.replace('/', '').replace('-', '')
    return int(ds)

def date_time_to_int(dt):
    return date_str_to_int(dt.strftime('%Y%m%d'))
