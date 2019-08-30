# -*- coding: utf-8 -*-

import arrow
from app import db

from . import ALL_CONTRACTS


class Ticker(db.Document):
    _id = db.StringField()
    ex = db.StringField(required=True)
    contract = db.StringField(required=True)
    last = db.FloatField(required=True)
    change_percentage = db.FloatField(required=True)
    funding_rate = db.FloatField(required=True)
    funding_rate_indicative = db.FloatField(required=True)
    mark_price = db.FloatField(required=True)
    index_price = db.FloatField(required=True)
    total_size = db.FloatField(required=True)
    volume_24h = db.FloatField(required=True)
    volume_24h_usd = db.FloatField(required=True)
    volume_24h_btc = db.FloatField(required=True)
    quanto_base_rate = db.FloatField(required=True)
    time = db.DateTimeField(required=True)

    meta = {'db_alias': 'market', 'collection': 'ticker'}

    def to_json(self, key=True):
        if key:
            return {
                "ex": self.ex.upper(),
                "contract": self.contract.upper(),
                "last": self.last,
                "change_percentage": self.change_percentage,
                "funding_rate": self.funding_rate,
                "funding_rate_indicative": self.funding_rate_indicative,
                "mark_price": self.mark_price,
                "index_price": self.index_price,
                "total_size": self.total_size,
                "volume_24h": self.volume_24h,
                "volume_24h_usd": self.volume_24h_usd,
                "volume_24h_btc": self.volume_24h_btc,
                "quanto_base_rate": self.quanto_base_rate,
                "time": arrow.get(self.time).float_timestamp,
            }
        else:
            return [
                arrow.get(self.time).float_timestamp,
                self.last,
                self.change_percentage,
                self.funding_rate,
                self.funding_rate_indicative,
                self.mark_price,
                self.index_price,
                self.total_size,
                self.volume_24h,
                self.volume_24h_usd,
                self.volume_24h_btc,
                self.quanto_base_rate,
            ]

    def __repr__(self):
        return '<Trade ex:\'%s\', contract:\'%s\'>' % (self.ex, self.contract)

    @staticmethod
    def get_within(hour=1, limit=10, ex=None, contract=None, key=True):
        '''
        获取时间区间内的数据
        :param hour:
        :return:
        '''
        now = arrow.now()
        start_time = now.shift(hours=-hour)
        query = Ticker.objects.filter(time__gte=start_time.datetime)
        if ex:
            query = query.filter(ex=ex)
        if contract:
            query = query.filter(contract=contract)
        if limit:
            query = query.limit(limit)

        data_list = query.all()
        result = []
        if data_list:
            for data in data_list:
                result.append(data.to_json(key))

        return result
