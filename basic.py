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
import yfinance as yf


input = pd.read_csv("C:\\Users\\Sahil Khare\\Desktop\\trading strategy project\\Input.csv")

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
            #time.sleep(2)
            print("Analytics data retrieved successfully for:" + scripname)
            run=1
        except:
            run=0
            print("Analytics data retrieval unsuccessful...Trying again")
            attempt=attempt+1
        
    return output



def get_historical_data(scripname,startdate,enddate):
    print("getting historical data for scrip: "+scripname)
    query = yf.Ticker(scripname)
    data = query.history(period="max")
    return data
                

    

def buy_sell_matrix(scripname,startdate,enddate,data_whole):
    
    buy = strategy_buy(scripname,startdate,data_whole)
    sell = strategy_sell(scripname,startdate,data_whole)
    data = data_whole.loc[startdate:enddate]
    output = pd.DataFrame(columns=['buy','sell','CP'])
    for index,each_date_data in data.iterrows():
        buy = strategy_buy(scripname,index,data_whole)
        sell = strategy_sell(scripname,index,data_whole)
        output.at[index,'CP'] = each_date_data["Close"]
        if (each_date_data["Close"]<buy):
            output.at[index,'buy'] = 1            
        else:
            output.at[index,'buy'] = 0
        if (each_date_data["Close"]>sell):
            output.at[index,'sell'] = 1
        else:
            output.at[index,'sell'] = 0
    return output

def get_profit_loss(data,account_start=10000):
    in_position = 0
    account=account_start
    current_value = account
    output = pd.DataFrame(columns=['transaction','CP'])
    current_value_arr = pd.DataFrame()
    for index,each_date_data in data.iterrows():
        if (each_date_data['buy']==1 and account -  each_date_data['CP'] > 0):
            account = account -  each_date_data['CP']
            output.at[index,'transaction'] = "buy"
            output.at[index,'CP'] = each_date_data['CP']
            in_position =in_position +1
        elif(in_position>0 and each_date_data['sell']==1):
            account = account + each_date_data['CP']
            in_position =in_position -1
            output.at[index,'transaction'] = "sell"
            output.at[index,'CP'] = each_date_data['CP']            
        current_value = each_date_data['CP']*in_position+account
        current_value_arr.at[index,'Value'] = current_value
    print("cuurentval = "+str(current_value))    
    profit = current_value- account_start 
    index = data.index
    delta = (max(index)-min(index))
    number_of_years = delta.days/365
    rate_of_return = ((current_value/account_start)**(1/number_of_years)-1)*100
    return account,in_position,current_value,profit,output,rate_of_return,number_of_years,current_value_arr

def get_nth_percentile(n,data):
    close_n_perc = np.percentile(data['Close'],n)
    return close_n_perc  



def data_required(scripname,startdate,enddate):
    return (get_historical_data(scripname,startdate+timedelta(-10),enddate))


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

scripname="RELIANCE.NS"
startdate='2019-01-01'
start = datetime.strptime(startdate, '%Y-%m-%d')
enddate='2020-04-03'
end = datetime.strptime(enddate, '%Y-%m-%d')

    
data = get_historical_data(scripname,start,end)
data = data_required(scripname,start,end)
#data['Close'].plot()


data1 = buy_sell_matrix(scripname,datetime.date(start),datetime.date(end),data)         
account_cash,stocks_held,value_stock,profit,buy_sell_timeframe,rate,duration,value_arr = get_profit_loss(data1)
value_arr['Value'].plot()





    
    
        
    

    
    
            
    

    



 

