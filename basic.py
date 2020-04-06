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
from datetime import datetime,timedelta

input = pd.read_csv("C:\\Users\\Sahil Khare\\Desktop\\trading strategy project\\Input.csv")
close_min_arr = np.array([])
close_min_90_perc_arr = np.array([])
close_min_50_perc_arr = np.array([])
close_min_10_perc_arr = np.array([])
run=0
attempt=1
while (not(run)):
    try:
        print("try="+str(attempt))
        if(attempt>100):
            break
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
                close_min_90_perc_arr = np.append(close_min_90_perc_arr,2147483647)    
                close_min_50_perc_arr = np.append(close_min_50_perc_arr,2147483647)
                close_min_10_perc_arr = np.append(close_min_10_perc_arr,2147483647)
                close_min_arr = np.append(close_min_arr,2147483647)
            time.sleep(2)
            print(close_min_arr)
            run=1
            
    except:
        run=0
        attempt=attempt+1

    
input["close_min"] = close_min_arr    
input["close_min_50_perc"] = close_min_50_perc_arr
input["close_min_90_perc"] = close_min_90_perc_arr 
input["close_min_10_perc"] = close_min_10_perc_arr 

input["Score"]=(input["close_min_10_perc"]-input["buy_price"])/input["close_min_10_perc"]   

input.to_excel("C:\\Users\\Sahil Khare\\Desktop\\trading strategy project\\output.xlsx")


def get_analytics_data(scripname,startdate,enddate):
    print("getting analytics data for scrip: "+scripname)
    run=0
    attempt=1
    while (not(run)):
        try:
            print("attempt="+str(attempt))
            if(attempt>100):
                break
            data = get_history(symbol=scripname, start=startdate, end=enddate)
            close_min = np.array(data[['Close']].min())
            close_min_90_perc = np.percentile(data['Close'],90)
            close_min_50_perc = np.percentile(data['Close'],50)
            close_min_10_perc = np.percentile(data['Close'],10)
            output = pd.DataFrame();
            output["close_min"] = close_min
            output["close_min_90_perc"] = close_min_90_perc
            output["close_min_50_perc"] = close_min_50_perc
            output["close_min_10_perc"] = close_min_10_perc
            time.sleep(2)
            print("Analytics data retrieved successfully for:" + scripname)
            run=1
        except:
            run=0
            print("Analytics data retrieval unsuccessful...Trying again")
            attempt=attempt+1
        
    return output

def get_nth_percentile(scripname,n,startdate,enddate):
    print("getting analytics data for scrip: "+scripname)
    run=0
    attempt=1
    while (not(run)):
        try:
            print("attempt="+str(attempt))
            if(attempt>100):
                break
            data = get_history(symbol=scripname, start=startdate, end=enddate)
            close_n_perc = np.percentile(data['Close'],n)
            time.sleep(2)
            print("Nth percentile data retrieved successfully for:" + scripname)
            run=1
        except:
            run=0
            print("Nth percentile retrieval unsuccessful...Trying again")
            attempt=attempt+1
    return close_n_perc  

def get_historical_data(scripname,startdate,enddate):
    print("getting historical data for scrip: "+scripname)
    run=0
    attempt=1
    while (not(run)):
        try:
            print("attempt="+str(attempt))
            if(attempt>100):
                break
            data = get_history(symbol=scripname, start=startdate, end=enddate)
            print("Historical data retrieved successfully for:" + scripname)
            run=1
        except:
            run=0
            print("Data retrieval unsuccessful...Trying again for Scrip: "+scripname)
            attempt=attempt+1
    return data
                

    

def buy_sell_matrix(scripname,startdate,enddate):
    buy = strategy_buy(scripname,startdate)
    sell = strategy_sell(scripname,startdate)
    data = get_historical_data(scripname,startdate,enddate)
    output = pd.DataFrame(columns=['buy','sell','CP'])
    for index,each_date_data in data.iterrows():
        buy = strategy_buy(scripname,index)
        sell = strategy_sell(scripname,index)
        print(each_date_data)
        print(index)
        print(type(output))
        output.at[index,'CP'] = each_date_data["Close"]
        if (each_date_data["Close"]<buy):
            output.at[index,'buy'] = 1            
        else:
            output.loc[index,'buy'] = 0
        if (each_date_data["Close"]>sell):
            output.at[index,'sell'] = 1
        else:
            output.at[index,'sell'] = 0
    return output

def get_profit_loss(data,account_start=1000):
    in_position = 0
    account=account_start
    current_value = account
    for index,each_date_data in data.iterrows():
        if (each_date_data['buy']==1 and account -  each_date_data['CP'] > 0):
            account = account -  each_date_data['CP']
            print(index)
            print("buy")
            in_position =in_position +1
        elif(in_position>0 and each_date_data['sell']==1):
            account = account + each_date_data['CP']
            in_position =in_position -1
            print(index)
            print("sell")
        current_value = each_date_data['CP']*in_position+account
        print("cuurentval = "+str(current_value))
    return account,in_position,current_value,current_value- account_start 

scripname="SBIN"
startdate='2019-01-01'
start = datetime.strptime(startdate, '%Y-%m-%d')
enddate='2020-01-01'
end = datetime.strptime(enddate, '%Y-%m-%d')

d = get_historical_data("SBIN",start,end)    
data1 = buy_sell_matrix(scripname,start,end)         
pl = get_profit_loss(data1)

def strategy_buy(scripname,date):
    startdate = date + timedelta(-10)
    enddate = date
    return get_nth_percentile(scripname,10,startdate,enddate)

cp = strategy_buy("SBIN",end)

def strategy_sell(scripname,date):
    startdate = date + timedelta(-10)
    enddate = date
    return get_nth_percentile(scripname,60,startdate,enddate)


    
    
        
    

    
    
            
    

    



 

