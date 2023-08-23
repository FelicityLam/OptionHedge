#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-11-25 22:16:05
LastEditTime: 2022-11-26 22:15:51
FilePath: \QTA_option_proj\src\MarketData\MarketData.py
'''

class MarketData:

    def __init__(self, asset_category: list):
        assert len(asset_category) > 0, 'empty asset_category'
        self.asset_category = asset_category
        self.data = {}
        for _asset in self.asset_category:
            self.data[_asset] = {}
        
    def get_data(self, asset, code, start_date: int = 0, end_date: int = 22222222):
        return self.data[asset][code].loc[start_date:end_date]

    def add_data(self, asset, code, data):
        self.data[asset][code] = data
        
