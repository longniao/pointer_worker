# -*- coding: utf-8 -*-

import copy
import arrow


DEFAULT_DATA = dict(
    ex='', # 交易所
    contract='', # 交易对
    time=0, # 时间
    open=0, # 开盘价
    close=0, # 收盘价
    high=0, # 最高价
    low=0, # 最低价
    amount=0,  # 成交量，币量
    count=0,  # 成交笔数
    volume=0, # 成交额 即 sum(每一笔成交价 * 该笔的成交量)
    range='', # 时间区间 1m 1h 1d
)

class Kline(object):

    collection = 'kline'

    @staticmethod
    def format(data):
        '''
        格式化数据
        :param data:
        :return:
        '''
        new_data = copy.deepcopy(DEFAULT_DATA)
        new_data['ex'] = str(data['ex'])
        new_data['contract'] = str(data['contract']).lower()
        new_data['range'] = str(data['range']).lower()
        new_data['time'] = arrow.get(data['time']).datetime
        new_data['open'] = float(data['open'])
        new_data['close'] = float(data['close'])
        new_data['high'] = float(data['high'])
        new_data['low'] = str(data['low'])

        if 'amount' in data:
            new_data['amount'] = float(data['amount'])
        if 'count' in data:
            new_data['count'] = float(data['count'])

        new_data['volume'] = float(data['volume'])

        return new_data
