# -- coding: utf-8 --
"""
Created on Sat Apr  4 17:01:09 2020

@author: Sahil Khare
"""

#import libraries

from nsepy import get_history
from nsepy import get_quote
import numpy as np
from datetime import date
import pandas as pd
import time
from datetime import datetime,timedelta
import yfinance as yf
import os    
    

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
    print(" historical data for scrip: "+scripname+" Retrieved successfully")
    return data
                

    

def buy_sell_matrix(scripname,startdate,enddate,data_whole):
    data = data_whole.loc[startdate:enddate]
    output = pd.DataFrame(columns=['buy','sell','CP'])
    for index,each_date_data in data.iterrows():
        output.at[index,'CP'] = each_date_data["Close"]
        output.at[index,'buy'] = strategy_buy(scripname,index,data_whole)
        output.at[index,'sell'] = strategy_sell(scripname,index,data_whole)
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
    single_scrip_data = {'account': account,
                        'in_position': in_position,
                        'current_value': current_value,
                        'profit': profit,
                        'rate': rate_of_return,
                        'time': time,
                        'current_value_arr' : current_value_arr,
                        'output':output}
    return single_scrip_data



def get_nth_percentile(n,data):
    close_n_perc = np.percentile(data['Close'],n)
    return close_n_perc  



def data_required(scripname,startdate,enddate):
    return (get_historical_data(scripname,startdate+timedelta(-10),enddate))



    

def strategy_buy(scripname,date,data_whole):
    startdate = date + timedelta(-30)
    enddate = date
    l=0
    m=-30
    n=-5
    
    data_n = data_whole.loc[startdate:enddate]
    startdate = date + timedelta(n)
    data_n_mean = data_n['Close'].mean()

    data_m = data_whole.loc[startdate:enddate]
    startdate = date + timedelta(m)
    data_m_mean = data_m['Close'].mean()
    
    data_l = data_whole.loc[startdate:enddate]
    startdate = date + timedelta(l)
    data_l_mean = data_l['Close'].mean()
         
    if(data_n_mean<data_m_mean and data_m_mean > data_l_mean ):
        is_buy=1
    else:
        is_buy=0
    return is_buy
    

def strategy_sell(scripname,date,data_whole):
    startdate = date + timedelta(-30)
    enddate = date
    l=0
    m=-30
    n=-5
    
    data_n = data_whole.loc[startdate:enddate]
    startdate = date + timedelta(n)
    data_n_mean = data_n['Close'].mean()

    data_m = data_whole.loc[startdate:enddate]
    startdate = date + timedelta(m)
    data_m_mean = data_m['Close'].mean()
    
    data_l = data_whole.loc[startdate:enddate]
    startdate = date + timedelta(l)
    data_l_mean = data_l['Close'].mean()
    
    if(data_n_mean>data_m_mean and data_m_mean < data_l_mean):
        is_sell=1
    else:
        is_sell=0
    return is_sell


##converts string to date format  
def initialize_date(date):
    return datetime.strptime(date, '%Y-%m-%d')

##read input file for sccrips in scope
def read_input():
    cwd = os.getcwd()
    scripname_list = pd.read_csv(cwd+"\\Desktop\\trading strategy project\\Input.csv")['scrip']
    return scripname_list

def initialize(scripname_list):
    for i in range(0,len(scripname_list)):
        scripname_list[i] = scripname_list[i]+".NS"
    return scripname_list
        


##initialize dates between which you want to test your strategy
startdate = '2019-01-01'
enddate='2020-04-09'

##initializes date to date format
start = initialize_date(startdate)
end = initialize_date(enddate)



compare = {}
scripname_list = read_input()
scripname_list = initialize(scripname_list)

for scripname in scripname_list:
    try:
        print(scripname)
        data = data_required(scripname,start,end)
        data1 = buy_sell_matrix(scripname,datetime.date(start),datetime.date(end),data)         
        data2 = get_profit_loss(data1)
    
        compare[scripname] = data2
    except:
        print("No data found for: " + scripname)

for scripname in scripname_list:
    print(scripname)
    compare[scripname]['current_value_arr'].plot()






    
    
        
    

    
    
            
    

    



 

