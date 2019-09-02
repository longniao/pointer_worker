# -*- coding: utf-8 -*-

import tushare as ts

token = '0a4672439efefb2a6cf2940cce35055e6a3f0e7d381af939768f4e9d'
ts.set_token(token)
pro = ts.pro_api()
pro = ts.pro_api(token)

df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='1min', start_date='20190902', end_date='20190903')
# df = pro.coinlist(start_date='20180101', end_date='20181231')
# df = pro.coinexchanges()
#df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='60min', start_date='20190829', end_date='20190830')
# df = pro.coincap(trade_date='20170806')
# df = pro.coincap(trade_date='20190824')
#df = pro.btc_marketcap(start_date='20190801', end_date='20190902')
print(type(df))
print(df)

for index, row in df.iterrows():
    pass
    #  print(row)

if __name__ == '__main__':
    try:
        pass
    except KeyboardInterrupt:
        pass
