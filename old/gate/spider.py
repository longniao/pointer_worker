# -*- coding: utf-8 -*-

import asyncio
import logging
import json
import traceback
import time
from datetime import datetime
from aiowebsocket.converses import AioWebSocket

from pointer_spider.gate.parser import gate_parser


def decode_ws_payload(data):
    return json.loads(data.decode('utf-8'))

async def gate_spider():
    '''
    gate spider
    url: https://gateio.co/docs/futures/ws/index.html
    :return:
    '''
    print('gate_spider: start')
    uri = 'wss://fx-ws.gateio.ws/v4/ws'

    async with AioWebSocket(uri) as aws:
        converse = aws.manipulator

        # 客户端给服务端发送消息
        # 行情
        # await converse.send('{"time" : 123456, "channel" : "futures.tickers", "event": "subscribe", "payload" : ["BTC_USD","EOS_USD"]}')
        # 实时交易
        # await converse.send('{"time" : 123456, "channel" : "futures.trades", "event": "subscribe", "payload" : ["BTC_USD","EOS_USD"]}')
        # 深度
        # await converse.send('{"time" : 123456, "channel" : "futures.order_book", "event": "subscribe", "payload" : ["BTC_USD", "20", "0"]}')
        # 蜡烛图/K线
        #await converse.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["10s", "BTC_USD"]}')
        await converse.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["15m", "BTC_USD"]}')
        await converse.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["1h", "BTC_USD"]}')
        await converse.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["4h", "BTC_USD"]}')
        await converse.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["1d", "BTC_USD"]}')

        while True:
            data = await converse.receive()
            if data:
                data = decode_ws_payload(data)
                await gate_parser(data)
            print('{time}-Client receive.'.format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


if __name__ == '__main__':
    count = 0
    while True:
        try:
            asyncio.get_event_loop().run_until_complete(gate_spider())
            print('try')
        except KeyboardInterrupt as exc:
            print('KeyboardInterrupt')
            logging.info('Quit.')
            break
        except Exception as e:
            count += 1
            traceback.print_exc()
            print(e, "Try again %s times..." % count)
            continue

