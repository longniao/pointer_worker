# -*- coding: utf-8 -*-

import arrow
from app import db
from app.models.market import ALL_CONTRACTS


class Kdj(db.Document):
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
    kdj_k = db.FloatField(required=True)
    kdj_d = db.FloatField(required=True)
    kdj_j = db.FloatField(required=True)
    ctime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)
    utime = db.DateTimeField(required=True, default=arrow.utcnow().datetime)

    meta = {'db_alias': 'market', 'collection': 'indicator_kdj', 'strict': False}

    def to_json(self, key=True):
        if key:
            return {
                "ex": self.ex.upper(),
                "contract": self.contract.upper(),
                "freq": self.freq,
                "kdj_k": self.kdj_k,
                "kdj_d": self.kdj_d,
                "kdj_j": self.kdj_j,
                "time": arrow.get(self.time).float_timestamp,
                "ctime": arrow.get(self.ctime).float_timestamp,
            }
        else:
            return [
                arrow.get(self.time).float_timestamp,
                self.kdj_k,
                self.kdj_d,
                self.kdj_j,
            ]

    def __repr__(self):
        return '<Indicator Kdj ex:\'%s\', contract:\'%s\'>' % (self.ex, self.contract)

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
            raise Exception('error contract:', contract)

        query = Kdj.objects
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

        data_list = query.order_by("time").all()
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
        indicator = Kdj.objects(ex=data['ex'], contract=data['contract'], freq=data['freq'], time=data['time']).first()

        if not indicator:
            return Kdj(**data).save()
        else:
            # 只更新当天的，过去的数据不用改变，所以不用更新
            new_time = arrow.get(data['time']).datetime
            old_time = arrow.get(indicator.time).datetime
            if new_time == old_time:
                update_data = dict()
                if 'kdj_k' in data and data['kdj_k'] != indicator.kdj_k:
                    update_data['kdj_k'] = data['kdj_k']
                if 'kdj_d' in data and data['kdj_d'] != indicator.kdj_d:
                    update_data['kdj_d'] = data['kdj_d']
                if 'kdj_j' in data and data['kdj_j'] != indicator.kdj_j:
                    update_data['kdj_j'] = data['kdj_j']
                if update_data:
                    print('indicator kdj update:', indicator._id, update_data)
                    update_data['utime'] = arrow.utcnow().datetime
                    Kdj.objects(_id=indicator._id).update_one(**update_data)
            return True
