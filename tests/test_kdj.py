# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import arrow
import tushare as ts
import pandas as pd
from app.indicators.expert import KDJZJ
from app.indicators.technology.countertrend import KDJ

pd.set_option('display.max_rows',None)
token = '0a4672439efefb2a6cf2940cce35055e6a3f0e7d381af939768f4e9d'
ts.set_token(token)
pro = ts.pro_api()
pro = ts.pro_api(token)

df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='daily', start_date='20190808', end_date='20190908')
# df = pro.coinlist(start_date='20180101', end_date='20181231')
# df = pro.coinexchanges()
# df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='60min', start_date='20190829', end_date='20190830')
# df = pro.coincap(trade_date='20170806')
# df = pro.coincap(trade_date='20190820')
# df = pro.btc_marketcap(start_date='20130801', end_date='20190905')

df.sort_values(by="date", inplace=True)
print(df)

df_kdj = KDJ(df)
print(df_kdj)

df = pd.concat([df,df_kdj], axis=1)
print(df)

df = df.dropna(axis=0,how='any')

for index, row in df.iterrows():
    if 'KDJ_D' in row and row['KDJ_D']:
        data = dict(
            ex='',
            contract='',
            freq='',
            time=arrow.get(row['date']).datetime,
            kdj_k=row['KDJ_K'],
            kdj_d=row['KDJ_D'],
            kdj_j=row['KDJ_J'],
        )
        print(data)

if __name__ == '__main__':
    try:
        pass
    except KeyboardInterrupt:
        pass
