# -*- coding: utf-8 -*-

import arrow
import tushare
from app.models.market.kline import Kline
from app.models.market.capital import Capital

token = '0a4672439efefb2a6cf2940cce35055e6a3f0e7d381af939768f4e9d'
tushare.set_token(token)
tushare_pro = tushare.pro_api()

def collect_kline(exchange, symbol, freq):
    '''
    获取数字货币行情数据，目前支持币币交易和期货合约交易。如果是币币交易，exchange参数请输入huobi,okex,binance,bitfinex等。如果是期货，exchange参数请输入future_xxx，比如future_okex，future_bitmex。
    :param exchange:
    :param symbol:
    :param freq:
    :return:
    '''
    now = arrow.now()
    end_date = now.format('YYYYMMDD')
    start_date = now.shift(days=-1).format('YYYYMMDD')

    print(exchange, symbol, freq, start_date, end_date)
    df = tushare_pro.coinbar(exchange=exchange, symbol=symbol, freq=freq, start_date=start_date, end_date=end_date)
    for index, row in df.iterrows():
        data = dict(
            ex=exchange,
            contract=symbol,
            freq=freq,
            time=row['date'],
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close'],
            volume=row['vol'],
        )
        # print(data)
        Kline.insert_data(data)

    return True


def collect_btc_marketcap(start_date=None, end_date=None):
    '''
    数字货币每日市值
    :param start_date:
    :param end_date:
    :return:
    {
        "func":"spider.tushare_spider.collect_btc_marketcap",
        "args": ["20190820"],
        "trigger": "date",
        "run_date":"2019-09-04 11:51:40"
    }
    '''
    if not end_date:
        end_date = arrow.now().format('YYYYMMDD')
    if not start_date:
        start_date = arrow.now().shift(days=-7).format('YYYYMMDD')

    df = tushare_pro.btc_marketcap(start_date=start_date, end_date=end_date)

    for index, row in df.iterrows():
        data = dict(
            coin=row['coin'],
            name=row['name'],
            marketcap=row['marketcap'],
            vol24=row['vol24'],
            date=row['trade_date'],
        )
        print(data)
        Capital.insert_data(data)

    return True
