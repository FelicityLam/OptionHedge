#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@Author: Felicity
@Email: felicity_lin@stu.pku.edu.cn
@Time: 2022-12-04 14:50
"""
import pandas as pd

data = {'A': [1, 2, 3],
        'B': [2, 3, 4],
        'C': [3, 4, 5]}
df1 = pd.DataFrame(data)
print(df1)
print(df1 / df1.loc[:, 'B'])
print(df1 / df1['B'])
print(df1.div(df1['B'], axis=0))
print(df1/df1)
print(df1.div(df1, axis=0))
