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
    ctime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)
    utime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)

    meta = {'db_alias': 'market', 'db_alias': 'market', 'collection': 'ticker'}

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
                "ctime": arrow.get(self.ctime).float_timestamp,
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
    def get_within(ex=None, contract=None, start_time=None, end_time=None, key=True):
        '''
        获取时间区间内的数据
        :param ex:
        :param contract:
        :param start_time:
        :param end_time:
        :param key:
        :return:
        '''
        query = Ticker.objects
        if ex:
            query = query.filter(ex=ex)
        if contract:
            query = query.filter(contract=contract)
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
        ticker = Ticker.objects(ex=data['ex'], contract=data['contract'], time=data['time']).first()

        if not ticker:
            return Ticker(**data).save()
        else:
            # 只更新当天的，过去的数据不用改变，所以不用更新
            new_time = arrow.get(data['time']).datetime
            old_time = arrow.get(ticker.time).datetime
            if new_time == old_time:
                update_data = dict()
                if 'open' in data and data['open'] != kline.open:
                    update_data['open'] = data['open']
                if 'high' in data and data['high'] != kline.high:
                    update_data['high'] = data['high']
                if 'low' in data and data['low'] != kline.low:
                    update_data['low'] = data['low']
                if 'close' in data and data['close'] != kline.close:
                    update_data['close'] = data['close']
                if update_data:
                    print('kline update:', kline._id, update_data)
                    update_data['utime'] = arrow.utcnow().datetime
                    Kline.objects(_id=kline._id).update_one(**update_data)
            return True
