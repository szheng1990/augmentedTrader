'''
@author: Shu Zheng
@contact: zhengshu@mit.edu
@summary: market simulator that automatically takes in and generates orders, and computes performance parameters

@input: orders in .csw format
@returns: key performance parameters such as volitility, cumulative return, daily return, and sharpe ratio

'''

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import numpy as np
import math

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

import csv

def get_market_price(symbol, time):
    symbol = symbol
    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    dataobj =da.DataAccess('Yahoo')
    raw_data = dataobj.get_data([time], [symbol], keys)
    close_data = dict(zip(keys, raw_data))["close"]
    
    close_data = close_data.fillna(method = 'ffill')
    close_data = close_data.fillna(method = 'bfill')
    close_data = close_data.fillna(1.0)
    
    market_price = np.array(close_data)[0,0]
    #print market_price
    return market_price
    

# read in csv order file
orders = pd.read_csv("orders.csv",names=['year','month','day','sym','order','qtt'],header=None)

orders = orders.sort(columns=['year','month','day'],ascending=1)

orders = orders.values

# convert the first three columns to datetime
order_times = [dt.datetime(orders[row,0],orders[row,1],orders[row,2],16) for row in range(len(orders))]

# get cash for each day

start_cash = 100000

NYSE_times = du.getNYSEdays(order_times[0], order_times[-1], dt.timedelta(hours=16))

cash_array = np.empty((len(NYSE_times),3),dtype="object")

cash_array[:,0] = NYSE_times

cash_array[0,1] = start_cash

#print cash_array

last_row = 0

for i in range(len(orders)):
    row, column = np.where(cash_array == order_times[i])
    row = row[0]
    cash_array[last_row:row,1] = cash_array[last_row,1]
    share = orders[i,5]
    price = get_market_price(orders[i,3],order_times[i])
    if orders[i,4] == "Buy":           
        cash_array[row,1] = cash_array[last_row,1] - share*price
    else:#sell
        cash_array[row,1] = cash_array[last_row,1] + share*price
    last_row = row
    
cash_array[last_row:len(cash_array),1] = cash_array[last_row,1]

    

#print cash_array

'''get daily return'''
unique_stocks = np.unique(orders[:,3])

master_array = np.empty((len(NYSE_times),1),dtype="object")
master_array[:,0] = NYSE_times

for stock in unique_stocks:
    #0. generate share table for this stock
    share_array = np.empty((len(NYSE_times),2),dtype="object")
    share_array[0,0] = 0 #share start at zero
    #1. find dates when the order occur
    rows, columns = np.where(orders == stock)
    last_date_index = 0
    for row in rows:
        # find the timestamp in nyse table
        date = dt.datetime(orders[row,0],orders[row,1],orders[row,2],16)
        NYSE_date_index, column = np.where(cash_array == date)
        NYSE_date_index = NYSE_date_index[0]
        #fill in same values in between
        share_array[last_date_index:NYSE_date_index,0] = share_array[last_date_index,0]

        share = orders[row,5]
        if orders[row,4] == "Buy":
            share_array[NYSE_date_index,0] = share_array[last_date_index,0] + share
        else: # sell
            share_array[NYSE_date_index,0] = share_array[last_date_index,0] - share
        last_date_index = NYSE_date_index

    #fill in the rest of the dates till the global end
    share_array[last_date_index:len(share_array),0] = share_array[last_date_index,0]
    #fetch yahoo data within the entire time frame
    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    dataobj =da.DataAccess('Yahoo')
    raw_data = dataobj.get_data(NYSE_times, [stock], keys)
    close_data = dict(zip(keys, raw_data))["close"] # same size as share_array
    
    close_data = close_data.fillna(method = 'ffill')
    close_data = close_data.fillna(method = 'bfill')
    close_data = close_data.fillna(1.0)

    for j in range(len(share_array)):
        share_array[j,1] = share_array[j,0] * np.array(close_data)[j,0]
    

    # append to master array to daily returns for that stock
    master_array = np.hstack((master_array,share_array))

print master_array[:,3:]


# calculate grand daily return (cash+return)
for i in range(len(master_array)):
    total_return = 0
    for j in range(len(master_array[i])):
        if j > 0 and j % 2 == 0:
            total_return += master_array[i,j]
    cash_array[i,2] = total_return + cash_array[i,1] #cash + return

#print len(cash_array)==len(master_array)

#print cash_array


#normalize data


daily_return = []
daily_return.append(0.0)
for i in range(1,len(cash_array)):
    tmp = cash_array[i,2]/cash_array[i-1,2] - 1
    daily_return.append(tmp)


daily_return = np.array(daily_return).reshape((len(cash_array),1))

vol = daily_return.std()
mean_daily = daily_return.mean()
sharpe = math.sqrt(252)*mean_daily/vol
cum_ret = cash_array[len(cash_array)-1,2]/cash_array[0,2]

print cash_array

print (sharpe, cum_ret,vol,mean_daily)