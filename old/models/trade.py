# -*- coding: utf-8 -*-

import copy
import arrow


DEFAULT_DATA = dict(
    ex='',
    contract='',
    id='',
    time=0,
    price=0,
    amount=0,
    type='',
)

class Trade(object):

    collection = 'trade'

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
        new_data['id'] = str(data['id'])
        new_data['time'] = arrow.get(data['time']).datetime
        new_data['price'] = float(data['price'])
        new_data['amount'] = float(data['amount'])
        new_data['type'] = str(data['type'])

        return new_data
