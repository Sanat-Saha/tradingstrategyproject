# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 04:26:29 2020

these file contains several strategies
@author: Sahil Khare
"""

'''Strategy # 1 percentile strategy'''

def strategy_buy(scripname,date,data_whole):
    startdate = date + timedelta(-3)
    enddate = date
    data = data_whole.loc[startdate:enddate]
    return get_nth_percentile(10,data)

def strategy_sell(scripname,date,data_whole):
    startdate = date + timedelta(-3)
    enddate = date
    data = data_whole.loc[startdate:enddate]
    return get_nth_percentile(70,data)


