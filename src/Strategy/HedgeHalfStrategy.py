#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-12-02 22:40:02
LastEditTime: 2022-12-04 00:24:34
FilePath: \QTA_option_proj\src\Strategy\HedgeHalfStrategy.py
'''
import pandas as pd

from .BaseStrategy import BaseStrategy
import numpy as np


class HedgeHalfStrategy(BaseStrategy):
    # 下面的写法会无法输入 BaseStrategy的参数
    # def __init__(self):
    #     super().__init__()

    def cal_position(self):
        hedge_all_position = (-self.cash_greeks['cash_delta'] / self.spot_price).values
        trade_days = len(self.spot_position)
        position = np.zeros(trade_days)
        position[0] = hedge_all_position[0]
        for t in range(1, trade_days):
            position[t] = (hedge_all_position[t] + position[t - 1]) / 2
        position = pd.DataFrame(position, index=self.spot_price.index)
        position_w = self.hedge_weight.mul(position, axis=0)
        self.spot_position = round(position_w / self.multiplier) * self.multiplier