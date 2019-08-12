# -*- coding: utf-8 -*-

import asyncio
import pprint
import motor.motor_asyncio
import arrow

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

db = client.flask_mongo

collection = 'trade'

trade_data = dict(
    ex='',
    pair='',
    id='',
    time=0,
    price=0,
    amount=0,
    type='',
)

async def do_insert_many(data_list):
    datas = []
    if data_list:
        for data in data_list:
            data['id'] = str(data['id'])
            data['time'] = arrow.get(data['time']).datetime
            datas.append(data)

        result = await db[collection].insert_many(datas)
        print('inserted %d docs' % (len(result.inserted_ids),))

async def do_insert_one(data):
    if data:
        data['id'] = str(data['id'])
        data['time'] = arrow.get(data['time']).datetime

        await db[collection].insert_one(data)
        print('inserted one docs')
