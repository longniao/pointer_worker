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
    price = db.FloatField(required=True, default=0)
    vol24 = db.FloatField(required=True, default=0)
    supply = db.FloatField(required=True, default=0)
    time = db.DateTimeField(required=True)
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
                "time": self.time,
                "ctime": arrow.get(self.ctime).float_timestamp,
            }
        else:
            return [
                arrow.get(self.time).float_timestamp,
                self.name,
                self.marketcap,
                self.price,
                self.vol24,
                self.supply,
            ]

    def __repr__(self):
        return '<Trade name:\'%s\', marketcap:\'%s\'>' % (self.name, self.marketcap)

    @staticmethod
    def get_within(coin=None, date=None, start_time=None, end_time=None, key=True):
        '''
        获取时间区间内的数据
        :param coin:
        :param date:
        :param start_time:
        :param end_time:
        :param key:
        :return:
        '''
        query = Capital.objects
        if coin:
            query = query.filter(coin=coin)
        if date:
            query = query.filter(date=date)
        if freq:
            query = query.filter(freq=freq)
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
        if 'coin' not in data or 'marketcap' not in data or 'time' not in data:
            raise Exception('params missed')

        # 检测，防止重复插入
        capital = Capital.objects(coin=data['coin'], marketcap=data['marketcap'], time=data['time']).first()

        if not capital:
            return Capital(**data).save()
        else:
            # 只更新当天的，过去的数据不用改变，所以不用更新
            new_time = arrow.get(data['time']).datetime
            old_time = arrow.get(capital.time).datetime
            if new_time == old_time:
                update_data = dict()
                if 'marketcap' in data and data['marketcap'] != capital.marketcap:
                    update_data['marketcap'] = data['marketcap']
                if 'price' in data and data['price'] != capital.price:
                    update_data['price'] = data['price']
                if 'vol24' in data and data['vol24'] != capital.vol24:
                    update_data['vol24'] = data['vol24']
                if 'supply' in data and data['supply'] != capital.supply:
                    update_data['supply'] = data['supply']
                if update_data:
                    print('Capital update:', capital._id, update_data)
                    update_data['utime'] = arrow.utcnow().datetime
                    Capital.objects(_id=capital._id).update_one(**update_data)
            return True
