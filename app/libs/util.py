# -*- coding: utf-8 -*-

import gzip
import json
import pickle


def decode_ws_payload(m):
    '''
    解析websocket收到的数据包
    :param m:
    :return:
    '''
    if m.is_text:
        recvStr = m.data.decode("utf-8")
        return json.loads(recvStr)
    elif m.is_binary:
        recvStr = gzip.decompress(m.data)
        return json.loads(recvStr)
    else:
        return json.loads(m)

def encode_ws_payload(data):
    '''
    发送websocket数据包
    :param data:
    :return:
    '''
    return json.dumps(data)

def modeltoJson(obj):
    '''
    mysql model转dict
    :param obj:
    :return:
    '''
    if not obj:
        return []
    if isinstance(obj, list):
        result = []
        for o in obj:
            result.append(modeltoJson(o))
        return result
    else:
        return jobToJson(pickle.loads(obj.job_state))

def jobToJson(job):
    '''
    job对象转为json
    :param self:
    :param job:
    :return:
    '''
    if not job: return None

    return {
        "id": job['id'],
        "name": job['name'],
        "trigger": str(job['trigger']),
        "func": job['func'],
        "args": job['args'],
        "kwargs": job['kwargs'],
        "executor": job['executor'],
        "max_instances": job['max_instances'],
        "next_run_time": str(job['next_run_time']),
        "misfire_grace_time": job['misfire_grace_time'],
        "coalesce": job['coalesce'],
        "version": job['version'],
    }
