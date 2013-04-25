'''
author: Shu Zheng
contact: zhengshu@mit.edu
summary: rolling statistics of stock data from Yahoo

'''

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import numpy as np
import math

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

symbols = ['MSFT'] ############
keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
timestamps = du.getNYSEdays(dt.datetime(2010, 1, 1), dt.datetime(2010, 12, 31), dt.timedelta(hours=16))


dataobj =da.DataAccess('Yahoo')
raw_data = dataobj.get_data(timestamps, symbols, keys)
close_data = dict(zip(keys, raw_data))["actual_close"]

means = pd.rolling_mean(close_data,20)
stds = pd.rolling_std(close_data,20)
df_vals = ((close_data-means)/stds)

#print for quiz
ts = df_vals.index
for sym in symbols:
    for i in range(len(ts)):
        print (sym, ts[i], df_vals[sym].ix[ts[i]])


            

