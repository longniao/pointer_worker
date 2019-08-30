# -*- coding: utf-8 -*-

import arrow
from app.sdks.tushare_sdk import tushare_pro


def search_coinbar(exchange, symbol, freq):
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
    return True

    df = tushare_pro.coinbar(exchange=exchange, symbol=symbol, freq=freq, start_date=start_date, end_date=end_date)
    return df


