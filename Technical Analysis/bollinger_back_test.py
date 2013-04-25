'''

@author: Shu Zheng
@contact: zhengshu@mit.edu
@summary: automated order generator based on event studies on bollinger bands

@reads: Yahoo data 
'''


import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""


def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['close']
    
    #ts_market = df_close['SPY']
    means = pd.rolling_mean(df_close,20)
    stds = pd.rolling_std(df_close,20)
    df_vals = ((df_close-means)/stds)
    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_vals)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_vals.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_vals[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_vals[s_sym].ix[ldt_timestamps[i - 1]]
            f_marketprice_today = df_vals['SPY'].ix[ldt_timestamps[i]]
            f_marketprice_yest = df_vals['SPY'].ix[ldt_timestamps[i - 1]]

            if f_symprice_today <= -2.0 and f_symprice_yest >= -2.0 and f_marketprice_today >= 1.0:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events


if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1) ############
    dt_end = dt.datetime(2009, 12, 31) ############
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
        d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data)


    #create orders
    order_list = ""
    for s in ls_symbols:
        for i in range(len(ldt_timestamps)):
             if df_events[s].ix[ldt_timestamps[i]] == 1: 
                    #positive event detected->create a pair of orders
                    tmp1 = ' '.join(str(ldt_timestamps[i]).split(' ')[0].split('-'))
                    if i+5 < len(ldt_timestamps):
                        tmp2 = ' '.join(str(ldt_timestamps[i+5]).split(' ')[0].split('-'))
                    else:
                        tmp2 = ' '.join(str(ldt_timestamps[-1]).split(' ')[0].split('-'))
                    order_list+=tmp1+' '+str(s)+' '+'Buy 100 \n'
                    order_list+=tmp2+' '+str(s)+' '+'Sell 100 \n'
    print order_list
