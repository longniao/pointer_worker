# -*- coding: utf-8 -*-

import asyncio
import logging
import json
import gzip
from datetime import datetime
from aiowebsocket.converses import AioWebSocket

from pointer_spider.huobi import client_id
from pointer_spider.huobi.parser import huobi_parser


def decode_ws_payload(data):
    return json.loads(gzip.decompress(data).decode('utf-8'))

def encode_ws_payload(data):
    return json.dumps(data)

async def huobi_spider():
    uri = 'wss://api.huobi.pro/ws'

    async with AioWebSocket(uri) as aws:
        converse = aws.manipulator

        # 客户端给服务端发送消息
        #await converse.send('{ "sub": "market.ethbtc.kline.1min", "id": "%s" }' % client_id)
        #await converse.send('{ "sub": "market.btcusdt.depth.step1", "id": "%s" }' % client_id)
        await converse.send('{ "sub": "market.btcusdt.trade.detail", "id": "%s" }' % client_id)
        #await converse.send('{ "sub": "market.btcusdt.detail", "id": "%s" }' % client_id)

        while True:
            data = await converse.receive()
            if data:
                data = decode_ws_payload(data)
                await huobi_parser(data)
                print('{time}-Client receive.'.format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


if __name__ == '__main__':
    while True:
        try:
            print('start spider...')
            asyncio.get_event_loop().run_until_complete(spider())
        except KeyboardInterrupt as exc:
            print('KeyboardInterrupt')
            logging.info('Quit.')
            break
        except Exception as e:
            print(e, "Try again.")
            continue

