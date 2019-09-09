# -*- coding: utf-8 -*-

import arrow
import pickle
from app import db
from app.libs.util import modeltoJson


class Job(db.Document):
    '''
    next_run_time: 下次执行时间
    job_state: str 任务信息
    '''
    _id = db.StringField()
    next_run_time = db.FloatField(required=True)
    job_state = db.StringField(required=True)

    meta = {'db_alias': 'base', 'collection': 'jobs', 'strict': False}

    def to_json(self):
        return {
            "id": self._id,
            "next_run_time": arrow.get(self.next_run_time).float_timestamp,
            "job_state": self.job_state,
        }

    def __repr__(self):
        return '<Trade id:\'%s\', next_run_time:\'%s\'>' % (self._id, self.next_run_time)

    @staticmethod
    def get_list():
        '''
        获取数据
        '''
        datas = Job.objects.all()
        result = []
        for row in datas:
            row = modeltoJson(row)
            print('row:', row)
            result.append(row)
        return result
