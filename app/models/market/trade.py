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
    type = db.StringField(required=True)
    time = db.DateTimeField(required=True)
    ctime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)
    utime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)

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
            "type": self.type.upper(),
            "time": arrow.get(self.time).float_timestamp,
            "ctime": arrow.get(self.ctime).float_timestamp,
        }

    def __repr__(self):
        return '<Trade ex:\'%s\', contract:\'%s\'>' % (self.ex, self.contract)

    @staticmethod
    def get_within(ex=None, contract=None, type=None, start_time=None, end_time=None, key=True):
        '''
        获取时间区间内的数据
        :param ex:
        :param contract:
        :param type:
        :param start_time:
        :param end_time:
        :param key:
        :return:
        '''
        query = Trade.objects
        if ex:
            query = query.filter(ex=ex)
        if contract:
            query = query.filter(contract=contract)
        if type:
            query = query.filter(type=type)
        if start_time:
            start_time = arrow.get(start_time).datetime
            query = query.filter(time__gte=start_time)
        if end_time:
            end_time = arrow.get(end_time).datetime
            query = query.filter(time__lt=end_time)

        data_list = query.order_by("time").all()
        result = []
        if data_list:
            for data in data_list:
                result.append(data.to_json(key))

        return result

    @staticmethod
    def insert_data(data):
        if 'ex' not in data or 'contract' not in data or 'time' not in data:
            raise Exception('params missed')

        # 检测，防止重复插入
        trade = Trade.objects(ex=data['ex'], contract=data['contract'], time=data['time']).first()

        if not trade:
            return Trade(**data).save()
        else:
            return True

