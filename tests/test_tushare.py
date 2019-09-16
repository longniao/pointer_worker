# -*- coding: utf-8 -*-

import arrow
import tushare as ts

token = '0a4672439efefb2a6cf2940cce35055e6a3f0e7d381af939768f4e9d'
ts.set_token(token)
pro = ts.pro_api()
pro = ts.pro_api(token)

TUSHARE_EXCHANGE_DICT = {
    'huobi': 'huobi',
    'gateio': 'gate',
}

TUSHARE_CONTRACT_DICT = {
    'btcusdt': 'btc_usdt',
}

TUSHARE_FREQ_DICT = {
    '15min': '15m',
    '60min': '1h',
    'daily': '1d',
    'week': '7d',
}

df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='15min', start_date='20190905', end_date='20190909')
# df = pro.coinlist(start_date='20180101', end_date='20181231')
# df = pro.coinexchanges()
# df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='60min', start_date='20190829', end_date='20190830')
# df = pro.coincap(trade_date='20170806')
# df = pro.coincap(trade_date='20190820')
# df = pro.btc_marketcap(start_date='20130801', end_date='20190905')
print(type(df))
print(df)

for index, row in df.iterrows():
    data = dict(
        ex=TUSHARE_EXCHANGE_DICT.get('huobi'),
        contract=TUSHARE_CONTRACT_DICT.get('btcusdt'),
        freq=TUSHARE_FREQ_DICT.get('daily'),
        time=arrow.get(row['date']).datetime,
        open=row['open'],
        high=row['high'],
        low=row['low'],
        close=row['close'],
        volume=row['vol'],
    )
    print(data)


if __name__ == '__main__':
    try:
        pass
    except KeyboardInterrupt:
        pass
