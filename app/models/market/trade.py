# -*- coding: utf-8 -*-

import arrow
from app import db

from . import ALL_CONTRACTS

class Trade(db.Document):
    _id = db.StringField()
    ex = db.StringField(required=True)
    contract = db.StringField(required=True)
    id = db.StringField(requied=True)
    price = db.FloatField(requied=True)
    amount = db.FloatField(requied=True)
    time = db.DateTimeField(required=True)
    type = db.StringField(required=True)

    meta = {'db_alias': 'market', 'collection': 'trade'}

    def to_json(self):
        if not self.type:
            if self.amount > 0:
                self.type = 'buy'
            else:
                self.type = 'sell'

        return {
            "ex": self.ex.upper(),
            "contract": self.contract.upper(),
            "price": self.price,
            "amount": self.amount,
            "time": arrow.get(self.time).float_timestamp,
            "type": self.type.upper(),
        }

    def __repr__(self):
        return '<Trade ex:\'%s\', contract:\'%s\'>' % (self.ex, self.contract)

    @staticmethod
    def get_within(hour=1, limit=10, ex=None, contract=None, type=None):
        '''
        获取时间区间内的数据
        :param hour:
        :return:
        '''
        now = arrow.now()
        start_time = now.shift(hours=-hour)
        query = Trade.objects.filter(time__gte=start_time.datetime)
        if ex:
            query = query.filter(ex=ex)
        if contract:
            query = query.filter(contract=contract)
        if type:
            query = query.filter(type=type)
        if limit:
            query = query.limit(limit)

        data_list = query.all()
        result = []
        if data_list:
            for data in data_list:
                result.append(data.to_json())

        return result
