# -- coding: utf-8 --
"""
Created on Sat Apr  4 17:01:09 2020

@author: Sahil Khare
"""

from nsepy import get_history
from nsepy import get_quote
import numpy as np
from datetime import date
import pandas as pd
import time

input = pd.read_csv("C:\\Users\\Sahil Khare\\Desktop\\trading strategy project\\Input.csv")
close_min_arr = np.array([])
close_min_90_perc_arr = np.array([])
close_min_50_perc_arr = np.array([])
close_min_10_perc_arr = np.array([])
run=0
while (not(run)):
    try:
        for scripname in input["scrip"]:
            print(scripname)
            data = get_history(symbol=scripname, start=date(2020,2,15), end=date(2020,4,3))    
         
            try:
                close_min = np.array(data[['Close']].min())
                close_min_90_perc = np.percentile(data['Close'],90)
                close_min_50_perc = np.percentile(data['Close'],50)
                close_min_10_perc = np.percentile(data['Close'],10)
                close_min_arr = np.append(close_min_arr,close_min)
                close_min_90_perc_arr = np.append(close_min_90_perc_arr,close_min_90_perc)
                close_min_50_perc_arr = np.append(close_min_50_perc_arr,close_min_50_perc)
                close_min_10_perc_arr = np.append(close_min_10_perc_arr,close_min_10_perc)
            except:
                close_min_90_perc_arr = np.append(close_min_90_perc_arr,0)    
                close_min_50_perc_arr = np.append(close_min_50_perc_arr,0)
                close_min_10_perc_arr = np.append(close_min_10_perc_arr,0)
                close_min_arr = np.append(close_min_arr,0)
            time.sleep(2)
            print(close_min_arr)
            run=1
    except:
        run=0

    
input["close_min"] = close_min_arr    
input["close_min_50_perc"] = close_min_50_perc_arr
input["close_min_90_perc"] = close_min_90_perc_arr 
input["close_min_10_perc"] = close_min_10_perc_arr 

input["Score"]=(input["close_min_10_perc"]-input["buy_price"])/input["close_min_10_perc"]   

input.to_excel("C:\\Users\\Sahil Khare\\Desktop\\trading strategy project\\output.xlsx")