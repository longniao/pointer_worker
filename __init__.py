# -*- coding: utf-8 -*-

import asyncio
import pprint
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

db = client.flask_mongo

collection = db.market

trade_data = dict(
    ex='',
    pair='',
    id='',
    time=0,
    price=0,
    amount=0,
    type='',
)


async def do_insert_many(collection, data):
    result = await db[collection].insert_many(data)
    print('inserted %d docs' % (len(result.inserted_ids),))

async def do_insert_one(collection, data):
    await db[collection].insert_one(data)
    print('inserted one docs')
