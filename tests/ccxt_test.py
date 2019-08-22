# -*- coding: utf-8 -*-

import time
import ccxt

gateio = ccxt.gateio({
    'proxies': {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5h://127.0.0.1:1080'
    },
})

'''
symbol = 'ETH/USD'
timeframe = '5m'
limit = 300
since = bitmex.milliseconds() - limit * 60 * 1000
params = {'partial': False}
ret = bitmex.fetch_ohlcv(symbol, timeframe, since, 12*24, params)
print(ret)
'''

# print(huobi.id, huobi.load_markets())
'''
print(gateio.id)
markets = gateio.load_markets()
if markets:
    for market, detail in markets.items():
        if 'USD' in market:
            print(market)


ohlcvs = gateio.fetch_ohlcv('BTC/USDT', timeframe='1d', limit=100)
if ohlcvs:
    for ohlcv in ohlcvs:
        t = time.localtime(ohlcv[0]/1000)
        print(t, ohlcv)

tickers = gateio.fetch_ticker('BTC/USDT')
print(tickers)
'''

symbol = 'BTC/USDT'
print(symbol, gateio.fetch_ohlcv(symbol, '1d'))  # one day


