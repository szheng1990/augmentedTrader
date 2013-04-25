'''
@author: Shu Zheng
@contact: zhengshu@mit.edu

@summary: portfolio optimizer that optimizes on sharpe ratio based on historical Yahoo stock data 
'''

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import numpy as np
import math

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

class Optimizer:
    def __init__(self,start,end,symbols):
        self.start = start
        self.end = end
        self.symbols = symbols

        timeofday = dt.timedelta(hours=16)
        timestamps = du.getNYSEdays(start, end, timeofday)

        keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

        # initialize query and get portfolio close data
        dataobj =da.DataAccess('Yahoo')
        raw_data = dataobj.get_data(timestamps, symbols, keys)
        close_data = dict(zip(keys, raw_data))["close"]

        # normalize data, get number of days, convert close data into array
        close_data_array = close_data.values
        close_data_array = close_data_array / close_data_array[0,:]
        
        

        # get reference data "$SPX"
        ref = da.DataAccess('Yahoo')
        ref_data = ref.get_data(timestamps, ["$SPX"], keys)[2] #reference close data
        ref_data_array = ref_data.values
        ref_data_array = ref_data_array / ref_data_array[0,:]
        
        self.timestamps = timestamps
        self.close_data_array = close_data_array
        self.spx_returns = ref_data_array
        
        
        


    def simulate(self, allocation):
        # calculate a column of weighted total daily return
        close_data_array = self.close_data_array
        days = len(close_data_array)
        alloc = np.array(allocation).reshape((4,1))
        weighted_daily_return = np.array([np.dot(day,alloc)[0] for day in close_data_array]).reshape((days,1))


        # calculate daily return
        daily_return = []
        daily_return.append(0.0)
        for i in range(1,days):
            tmp = weighted_daily_return[i,0]/weighted_daily_return[i-1,0] - 1
            daily_return.append(tmp)
        daily_return = np.array(daily_return).reshape((days,1))
        #print daily_return

        vol = daily_return.std()
        mean_daily = daily_return.mean()
        sharpe = math.sqrt(252)*mean_daily/vol
        cum_ret = weighted_daily_return[days-1,0]

        return (vol, mean_daily, sharpe, cum_ret)

    def optimize(self):
        best = [0,[]]
        fraction = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        for a in fraction:
            for b in fraction:
                for c in fraction:
                    for d in fraction:
                        if a+b+c+d==1:
                            stats = self.simulate([a,b,c,d])
                            if stats[2] > best[0]:
                                best[0] = stats[2] #sharpe
                                best[1] = [a,b,c,d] #alloc
        return best


    def plot(self):
        best = self.optimize()
        close_data_array = self.close_data_array
        days = len(close_data_array)
        alloc = np.array(best[1]).reshape((4,1))
        port_returns = np.array([np.dot(day,alloc)[0] for day in close_data_array]).reshape((days,1))

        
        plt.clf()
        plt.plot(self.timestamps,port_returns)
        plt.plot(self.timestamps,self.spx_returns)
        plt.legend(["portfolio","$SPX"])
        plt.ylabel("Normalized Adjusted Close")
        plt.xlabel("Date")
        plt.savefig("comparison.pdf",format='pdf')
        
        



    

    

    

    

    
