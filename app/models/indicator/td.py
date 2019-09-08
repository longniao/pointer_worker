# -*- coding: utf-8 -*-

import arrow
from app import db
from . import ALL_CONTRACTS


class Td(db.Document):
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
    freq = db.StringField(required=True)
    time = db.DateTimeField(required=True)
    td_count = db.IntField(required=True)
    td_high = db.IntField(required=True)
    td_low = db.IntField(required=True)
    td_close = db.IntField(required=True)
    ctime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)
    utime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)

    meta = {'collection': 'indicator_td', 'strict': False}

    def to_json(self, key=True):
        if key:
            return {
                "ex": self.ex.upper(),
                "contract": self.contract.upper(),
                "freq": self.freq,
                "td_count": self.td_count,
                "td_high": self.td_high,
                "td_low": self.td_low,
                "td_close": self.td_close,
                "time": arrow.get(self.time).float_timestamp,
                "ctime": arrow.get(self.ctime).float_timestamp,
            }
        else:
            return [
                arrow.get(self.time).float_timestamp,
                self.td_count,
                self.td_high,
                self.td_low,
                self.td_close,
            ]

    def __repr__(self):
        return '<Indicator Td ex:\'%s\', contract:\'%s\'>' % (self.ex, self.contract)

    @staticmethod
    def get_within(ex=None, contract=None, freq=None, start_time=None, end_time=None, limit=None, key=True):
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

        query = Td.objects
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

        data_list = query.order_by("time").find()
        if limit:
            data_list = data_list[:limit]

        result = []
        if data_list:
            for data in data_list:
                result.append(data.to_json(key))

        return result

    @staticmethod
    def insert_data(data):
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
        indicator = Td.objects(ex=data['ex'], contract=data['contract'], freq=data['freq'], time=data['time']).first()

        if not indicator:
            return Td(**data).save()
        else:
            # 只更新当天的，过去的数据不用改变，所以不用更新
            new_time = arrow.get(data['time']).datetime
            old_time = arrow.get(indicator.time).datetime
            if new_time == old_time:
                update_data = dict()
                if 'td_count' in data and data['td_count'] != indicator.open:
                    update_data['td_count'] = data['td_count']
                if 'td_high' in data and data['td_high'] != indicator.high:
                    update_data['td_high'] = data['td_high']
                if 'td_low' in data and data['td_low'] != indicator.low:
                    update_data['td_low'] = data['td_low']
                if 'td_close' in data and data['td_close'] != indicator.close:
                    update_data['td_close'] = data['td_close']
                if update_data:
                    print('indicator td update:', indicator._id, update_data)
                    update_data['utime'] = arrow.utcnow().datetime
                    Td.objects(_id=indicator._id).update_one(**update_data)
            return True
