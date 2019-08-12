# -*- coding: utf-8 -*-

import asyncio
import logging
import json
from datetime import datetime
from aiowebsocket.converses import AioWebSocket

from pointer_spider.gate import client_id
from pointer_spider.gate.parser import gate_parser


def decode_ws_payload(data):
    return json.loads(data.decode('utf-8'))

async def gate_spider():
    print('gate_spider: start')
    uri = 'wss://ws.gateio.ws/v3/'

    async with AioWebSocket(uri) as aws:
        converse = aws.manipulator

        # 客户端给服务端发送消息
        await converse.send('{"id":%s,"method":"server.ping","params":[]}' % client_id)
        await converse.send('{"id":%s, "method":"server.time", "params":[]}' % client_id)
        await converse.send('{"id":%s, "method":"trades.subscribe", "params":["BTC_USDT", "EOS_USDT"]}' % client_id)
        #await converse.send('{"id":%s, "method":"depth.subscribe", "params":["BTC_USDT", 5, "0.0001"]}' % client_id)

        while True:
            data = await converse.receive()
            data = decode_ws_payload(data)
            await gate_parser(data)
            print('{time}-Client receive.'.format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


if __name__ == '__main__':
    count = 0
    while True:
        try:
            asyncio.get_event_loop().run_until_complete(spider())
            print('try')
        except KeyboardInterrupt as exc:
            print('KeyboardInterrupt')
            logging.info('Quit.')
            break
        except Exception as e:
            count += 1
            print(e, "Try again %s times..." % count)
            continue

