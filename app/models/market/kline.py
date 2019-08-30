# -*- coding: utf-8 -*-

import arrow
from app import db


class Kline(db.Document):
    '''
    ex: str 交易所
    contract: str 交易对
    open: float 开盘价
    high: float 最高价
    low: float 最低价
    close: float 收盘价
    volume: float 成交量
    count: int 成交笔数（默认不展示，有些交易所没有此项数据，若需要请在fields里添加）
    amount: float 成交额 (默认不展示,需在fields里添加上，有些交易所没有此项数据)
    freq: str 行情频率
    time: datetime 行情时间
    '''
    _id = db.StringField()
    ex = db.StringField(required=True)
    contract = db.StringField(required=True)
    open = db.FloatField(required=True)
    high = db.FloatField(required=True)
    low = db.FloatField(required=True)
    close = db.FloatField(required=True)
    volume = db.FloatField(required=True)
    count = db.FloatField(required=True, default=0)
    amount = db.FloatField(required=True, default=0)
    freq = db.StringField(required=True)
    time = db.DateTimeField(required=True)
    ctime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)
    utime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)

    meta = {'collection': 'kline'}

    def to_json(self, key=True):
        if key:
            return {
                "ex": self.ex.upper(),
                "contract": self.contract.upper(),
                "open": self.open,
                "high": self.high,
                "low": self.low,
                "close": self.close,
                "volume": self.volume,
                "range": self.range,
                "time": arrow.get(self.time).float_timestamp,
            }
        else:
            return [
                arrow.get(self.time).float_timestamp,
                self.open,
                self.high,
                self.low,
                self.close,
                self.volume,
            ]

    def __repr__(self):
        return '<Trade ex:\'%s\', contract:\'%s\'>' % (self.ex, self.contract)

    @staticmethod
    def get_within(ex=None, contract=None, freq=None, hour=None, key=True):
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
            if 'open' in data:
                kline.open = data['open']
            if 'high' in data:
                kline.high = data['high']
            if 'low' in data:
                kline.low = data['low']
            if 'close' in data:
                kline.close = data['close']
            return kline.save()
