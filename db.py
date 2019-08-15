# -*- coding: utf-8 -*-

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

db = client.flask_mongo


async def do_insert_many(model, data_list):
    '''
    批量插入
    :param model:
    :param data_list:
    :return:
    '''
    if data_list:
        result = await db[model.collection].insert_many(data_list)
        print('inserted %s %s' % (len(result.inserted_ids), model.collection))


async def do_insert_one(model, data):
    '''
    单条数据插入
    :param model:
    :param data:
    :return:
    '''
    if data:
        await db[model.collection].insert_one(data)
        print('inserted one %s' % model.collection)

async def do_find(model, data={}):
    '''
    查询
    :param model:
    :param data:
    :return:
    '''
    result = await db[model.collection].find(data)
    print('query %s' % model.collection)
    return result

async def do_find_one(model, filter):
    '''
    查询
    :param model:
    :param filter:
    :return:
    '''
    result = await db[model.collection].find_one(filter)
    print('find one %s' % model.collection)
    return result

async def do_update_one(model, filter, update):
    '''
    更新
    :param model:
    :param filter:
    :param update:
    :return:
    '''
    print('update one %s' % model.collection, filter)
    await db[model.collection].update_one(filter, {
        '$set': update
    })
