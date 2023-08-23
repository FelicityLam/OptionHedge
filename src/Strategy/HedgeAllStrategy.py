#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-12-02 22:40:02
LastEditTime: 2022-12-04 00:23:54
FilePath: \QTA_option_proj\src\Strategy\HedgeAllStrategy.py
'''
from .BaseStrategy import BaseStrategy


class HedgeAllStrategy(BaseStrategy):


    def cal_position(self):
        # cash_delta / index点位，乘上weight，再按multiplier规整
        position = -self.cash_greeks['cash_delta']/self.spot_price
        position_w = self.hedge_weight.mul(position, axis=0)
        self.spot_position = round(position_w/self.multiplier)*self.multiplier