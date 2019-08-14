# -*- coding: utf-8 -*-

import copy
import arrow


DEFAULT_DATA = dict(
    ex='',
    contract='',
    last=0,
    change_percentage=0,
    funding_rate=0,
    funding_rate_indicative=0,
    mark_price=0,
    index_price=0,
    total_size=0,
    volume_24h=0,
    volume_24h_usd=0,
    volume_24h_btc=0,
    quanto_base_rate=0,
    time=0,
)

class Ticker(object):

    collection = 'ticker'

    @staticmethod
    def format(data):
        '''
        格式化数据
        :param data:
        :return:
        '''
        new_data = copy.deepcopy(DEFAULT_DATA)

        new_data['ex'] = str(data['ex'])
        new_data['contract'] = str(data['contract'])
        new_data['last'] = float(data['last'])
        new_data['change_percentage'] = float(data['change_percentage'])
        new_data['funding_rate'] = float(data['funding_rate'])
        new_data['funding_rate_indicative'] = str(data['funding_rate_indicative'])
        new_data['mark_price'] = float(data['mark_price'])
        new_data['index_price'] = float(data['index_price'])
        new_data['total_size'] = float(data['total_size'])
        new_data['volume_24h'] = float(data['volume_24h'])
        new_data['volume_24h_btc'] = float(data['volume_24h_btc'])
        new_data['volume_24h_usd'] = float(data['volume_24h_usd'])
        new_data['quanto_base_rate'] = float(data['quanto_base_rate'])
        new_data['time'] = arrow.get(data['time']).datetime

        return new_data
