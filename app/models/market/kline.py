# -*- coding: utf-8 -*-

import arrow
from app import db
from . import ALL_CONTRACTS


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

    meta = {'db_alias': 'market', 'collection': 'kline', 'strict': False}

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
                "freq": self.freq,
                "time": arrow.get(self.time).float_timestamp,
                "ctime": arrow.get(self.ctime).float_timestamp,
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
        return '<Kline ex:\'%s\', contract:\'%s\'>' % (self.ex, self.contract)

    @staticmethod
    def get_within(ex=None, contract=None, freq=None, start_time=None, end_time=None, limit=None, order=None, key=True):
        '''
        获取时间区间内的数据
        :param ex:
        :param contract:
        :param freq:
        :param start_time:
        :param end_time:
        :param limit:
        :param key:
        :return:
        '''
        if contract not in ALL_CONTRACTS:
            raise Exception('error contract')

        query = Kline.objects
        if ex:
            query = query.filter(ex=ex)
        if contract:
            query = query.filter(contract=contract)
        if freq:
            query = query.filter(freq=freq)
        if start_time:
            start_time = arrow.get(start_time).datetime
            query = query.filter(time__gte=start_time)
        if end_time:
            end_time = arrow.get(end_time).datetime
            query = query.filter(time__lt=end_time)
        if order:
            query = query.order_by(order)

        data_list = query.all()
        if limit:
            data_list = data_list[:limit]

        result = []
        if data_list:
            for data in data_list:
                result.append(data.to_json(key))

        return result

    @staticmethod
    def insert_data(data, update_when_exist=True, update_fields=['open','high','low','close','volume']):
        '''
        新增数据
        :param data:
        :return:
        '''
        if 'ex' not in data or 'contract' not in data or 'freq' not in data or 'time' not in data:
            raise Exception('params missed')
        if data['contract'] not in ALL_CONTRACTS:
            raise Exception('error contract')

        # 检测，防止重复插入
        kline = Kline.objects(ex=data['ex'], contract=data['contract'], freq=data['freq'], time=data['time']).first()

        if not kline:
            return Kline(**data).save()
        else:
            if not update_when_exist:
                return False

            # 只更新当天的，过去的数据不用改变，所以不用更新
            new_time = arrow.get(data['time']).datetime
            old_time = arrow.get(kline.time).datetime
            if new_time == old_time:
                update_data = dict()
                if 'open' in data and data['open'] != kline.open and 'open' in update_fields:
                    update_data['open'] = data['open']
                if 'high' in data and data['high'] != kline.high and 'high' in update_fields:
                    update_data['high'] = data['high']
                if 'low' in data and data['low'] != kline.low and 'low' in update_fields:
                    update_data['low'] = data['low']
                if 'close' in data and data['close'] != kline.close and 'close' in update_fields:
                    update_data['close'] = data['close']
                if 'volume' in data and data['volume'] != kline.volume and 'volume' in update_fields:
                    update_data['volume'] = data['volume']
                if update_data:
                    print('kline update:', data['ex'], data['contract'], data['freq'], data['time'], update_data)
                    update_data['utime'] = arrow.utcnow().datetime
                    Kline.objects(_id=kline._id).update_one(**update_data)
            return True
