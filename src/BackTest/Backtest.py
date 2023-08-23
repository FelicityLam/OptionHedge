#!/usr/bin/env python
# coding=utf-8
'''
Author: LetheYE
email: mengjie_ye@stu.pku.edu.cn
Date: 2022-12-02 14:11:19
LastEditTime: 2022-12-03 23:22:29
FilePath: \QTA_option_proj\src\BackTest\Backtest.py
'''
import pandas as pd
from ..MarketData.test_data import test_data as market_data
import matplotlib.pyplot as plt
import os
import pandas as pd
from ..Option.BaseOption import BaseOption
from ..Strategy.BaseStrategy import BaseStrategy

class Backtest():
    
    def __init__(self, strategy: BaseStrategy, option: BaseOption):
        self.strategy = strategy
        self.option = option
        self.hedge_pnl_df: pd.DataFrame = None
        self.option_pnl_df: pd.DataFrame = None
    
    def portfolio_pnl_decompose(self):
        self.hedge_pnl_decompose()
        self.option_pnl_decompose()
        
    def hedge_pnl_decompose(self):
        self.hedge_pnl_df = self.strategy.pnl_decompose()
        return self.hedge_pnl_df
    
    def option_pnl_decompose(self):
        self.option_pnl_df = self.option.pnl_decompose()
        return self.option_pnl_df
    
    def report(self, to_save_dir = None):
        assert self.hedge_pnl_df is not None, 'Need to decompose hedge_pnl'
        self.report_hedge(to_save_dir)
        assert self.option_pnl_df is not None, 'Need to decompose option_pnl'
        assert len(self.hedge_pnl_df) == len(self.option_pnl_df), f'check the shape of self.hedge_pnl_df ({len(self.hedge_pnl_df)}) & self.option_pnl_df ({len(self.option_pnl_df)})'
        self.report_option(to_save_dir)
        self.report_portfolio(to_save_dir)
    
    def report_hedge(self, to_save_dir = None):
        date_str_list = [str(x) for x in self.hedge_pnl_df.index]
        to_plot_df = self.hedge_pnl_df.copy()
        to_plot_df.index = date_str_list
        tmp_is_trade_idx = [date_str_list.index(x) for x in to_plot_df[to_plot_df.is_trade==1].is_trade.values]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14,10), sharex=True, constrained_layout=True)
        to_plot_df[['CA', 'MA']].plot(axis=ax1, color=['darkblue', 'darkred'], alpha=0.7)
        for _i in tmp_is_trade_idx:
            ax1.axvline(x=_i, color='grey', ls='--', alpha=0.4)
        ax1_tw = ax1.twinx()
        to_plot_df['nav'].plot(axis=ax1_tw, color='black', label='nav')
        to_plot_df['delta_nav'].plot.area(ax=ax1_tw, color='blue', alpha=0.4, label='delta_nav', linewidth=0)
        ax1.set_title('Cash Account + Margin Account')
        ax1.legend(loc='upper right')
        ax1_tw.legend(loc='upper left')
        
        to_plot_df[['IC', 'TC']].plot(axis=ax2, color=['darkblue', 'darkred'], alpha=0.7)
        ax2_tw = ax2.twinx()
        to_plot_df['nav'].plot(axis=ax1_tw, color='black', label='nav')
        for _i in tmp_is_trade_idx:
            ax2.axvline(x=_i, color='grey', ls='--', alpha=0.4)
        to_plot_df['delta_nav'].plot.area(ax=ax2_tw, color='blue', alpha=0.4, label='delta_nav', linewidth=0)
        ax2.set_title('Interest Cost + Trading Cost')
        ax2.legend(loc='upper right')
        ax2_tw.legend(loc='upper left')
        if to_save_dir is not None:
            fig.savefig(os.path.join(to_save_dir, 'hedge_pnl_decompose.jpg'))
        else:
            plt.show()
            
    def report_option(self, to_save_dir = None):
        date_str_list = [str(x) for x in self.option_pnl_df.index]
        to_plot_df = self.option_pnl_df[['option_pnl', 'delta_pnl', 'gamma_pnl', 'theta_pnl', 'carry_pnl', 'disc_pnl', 'residual']].copy()
        to_plot_df.index = date_str_list
        # tmp_is_trade_idx = [date_str_list.index(x) for x in to_plot_df[to_plot_df.is_trade==1].is_trade.values]
        fig, ax= plt.subplots(figsize=(14,5), constrained_layout=True)
        to_plot_df.cumsum().plot(ax=ax)
        ax.set_title('option_pnl_decompose')
        if to_save_dir is not None:
            fig.savefig(os.path.join(to_save_dir, 'option_pnl_decompose.jpg'))
        else:
            plt.show() 
            
    def report_portfolio(self, to_save_dir = None):
        date_str_list = [str(x) for x in self.option_pnl_df.index]
        to_plot_df = pd.concat([self.hedge_pnl_df['delta_nav'], self.option_pnl_df['option_pnl']], axis=1).rename(columns={'nav': 'hedge_pnl'})
        to_plot_df['portfolio_pnl'] = to_plot_df['hedge_pnl'] + to_plot_df['option_pnl']
        fig, ax= plt.subplots(figsize=(14,5), constrained_layout=True)
        to_plot_df.cumsum().plot(ax=ax)
        ax.set_title('portfolio_pnl_decompose')
        if to_save_dir is not None:
            fig.savefig(os.path.join(to_save_dir, 'portfolio_pnl_decompose.jpg'))
        else:
            plt.show() 
        