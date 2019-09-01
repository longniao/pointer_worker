# -*- coding: utf-8 -*-

import arrow
from app import db


class Capital(db.Document):
    '''
    coin	str	货币代码
    name	str	货币名称
    marketcap	str	市值（美元）
    price	float	当前时间价格（美元）
    vol24	float	24小时成交额（美元）
    supply	float	流通总量
    date	str	交易日期
    ctime	datetime	数据采集时间
    '''
    _id = db.StringField()
    coin = db.StringField(required=True)
    name = db.StringField(required=True)
    marketcap = db.StringField(required=True)
    price = db.FloatField(required=True)
    vol24 = db.FloatField(required=True)
    supply = db.FloatField(required=True)
    date = db.DateTimeField(required=True)
    ctime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)
    utime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)

    meta = {'collection': 'capital', 'strict': False}

    def to_json(self, key=True):
        if key:
            return {
                "coin": self.coin.upper(),
                "name": self.name,
                "marketcap": self.marketcap,
                "price": self.price,
                "vol24": self.vol24,
                "supply": self.supply,
                "date": self.date,
                "ctime": arrow.get(self.ctime).float_timestamp,
            }
        else:
            return [
                arrow.get(self.date).float_timestamp,
                self.name,
                self.marketcap,
                self.price,
                self.vol24,
                self.supply,
            ]

    def __repr__(self):
        return '<Trade name:\'%s\', marketcap:\'%s\'>' % (self.name, self.marketcap)

    @staticmethod
    def get_within(coin=None, hour=None, key=True):
        '''
        获取时间区间内的数据
        :param ex:
        :param contract:
        :param freq:
        :param hour:
        :param key:
        :return:
        '''
        query = Kline.objects
        if ex:
            query = query.filter(ex=ex)
        if contract:
            query = query.filter(contract=contract)
        if freq:
            query = query.filter(freq=freq)
        if hour:
            now = arrow.now()
            start_time = now.shift(hours=-hour)
            query = query.filter(time__gte=start_time.datetime)

        data_list = query.order_by("time").all()
        result = []
        if data_list:
            for data in data_list:
                result.append(data.to_json(key))

        return result

    @staticmethod
    def insert_data(data):
        if 'ex' not in data or 'contract' not in data or 'freq' not in data or 'time' not in data:
            raise Exception('params missed')

        # 检测，防止重复插入
        kline = Kline.objects(ex=data['ex'], contract=data['contract'], freq=data['freq'], time=data['time']).first()

        if not kline:
            return Kline(**data).save()
        else:
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
                Kline.objects(_id=kline._id).update_one(**update_data)
            return True
