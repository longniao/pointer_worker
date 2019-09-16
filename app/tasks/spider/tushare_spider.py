# -*- coding: utf-8 -*-

import arrow
import tushare
from app.models.market.kline import Kline
from app.models.market.capital import Capital

token = '0a4672439efefb2a6cf2940cce35055e6a3f0e7d381af939768f4e9d'
tushare.set_token(token)
tushare_pro = tushare.pro_api()

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


class TushareClient(object):

    def kline(self, exchange, symbol, freq, start_date=None, end_date=None):
        '''
        获取数字货币行情数据，目前支持币币交易和期货合约交易。如果是币币交易，exchange参数请输入huobi,okex,binance,bitfinex等。如果是期货，exchange参数请输入future_xxx，比如future_okex，future_bitmex。
        :param exchange:
        :param symbol:
        :param freq:
        :param start_date:
        :param end_date:
        :return:
        '''
        if not end_date:
            end_date = arrow.now().format('YYYYMMDD')
        if not start_date:
            start_date = arrow.now().shift(days=-7).format('YYYYMMDD')

        print(exchange, symbol, freq, start_date, end_date)
        df = tushare_pro.coinbar(exchange=exchange, symbol=symbol, freq=freq, start_date=start_date, end_date=end_date)
        for index, row in df.iterrows():
            data = dict(
                ex=TUSHARE_EXCHANGE_DICT.get(exchange),
                contract=TUSHARE_CONTRACT_DICT.get(symbol),
                freq=TUSHARE_FREQ_DICT.get(freq),
                time=arrow.get(row['date'], tzinfo='Asia/Shanghai').datetime,
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['vol'],
            )
            # print(data)
            Kline.insert_data(data, update_fields=['volume'])

        return True


    def btc_marketcap(self, start_date=None, end_date=None):
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
                date=arrow.get(row['trade_date'], tzinfo='Asia/Shanghai').datetime,
            )
            print(data)
            Capital.insert_data(data)

        return True


client = TushareClient()

def collect_kline(exchange, symbol, start_date=None, end_date=None):
    '''
    采集K线
    :param exchange:
    :param symbol:
    :param start_date:
    :param end_date:
    :return:
    '''
    if not end_date:
        end_date = arrow.now().format('YYYYMMDD')
    if not start_date:
        start_date = arrow.now().shift(days=-7).format('YYYYMMDD')

    for key, value in TUSHARE_FREQ_DICT.items():
        client.kline(exchange, symbol, key, start_date, end_date)


def collect_btc_marketcap(start_date=None, end_date=None):
    '''
    采集BTC市值
    :param start_date:
    :param end_date:
    :return:
    '''
    if not end_date:
        end_date = arrow.now().format('YYYYMMDD')
    if not start_date:
        start_date = arrow.now().shift(days=-7).format('YYYYMMDD')

    client.btc_marketcap(start_date, end_date)


if __name__ == '__main__':
    try:
        collect_kline()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')

