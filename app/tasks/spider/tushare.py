# -*- coding: utf-8 -*-

import arrow
from app.sdks.tushare_sdk import tushare_pro
from app.models.market.kline import Kline
from app.models.market.capital import Capital


def collect_tushare_kline(exchange, symbol, freq):
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


def collect_tushare_capital(date=None):
    '''
    数字货币每日市值
    获取数字货币每日市值数据，该接口每隔6小时采集一次数据，所以当日每个品种可能有多条数据，用户可根据实际情况过滤截取使用。
    :return:
    '''
    if not date:
        date = arrow.now().shift(days=-1).format('YYYYMMDD')

    print(date)
    df = tushare_pro.coincap(trade_date=date)
    print(df)
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
