# -*- coding: utf-8 -*-

import asyncio
import logging
import json
import traceback
import tushare as ts
from datetime import datetime

from pointer_worker.tushare.parser import tushare_parser

ts.set_token('0a4672439efefb2a6cf2940cce35055e6a3f0e7d381af939768f4e9d')
pro = ts.pro_api()

df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')

async def tushare_spider():
    '''
    tushare spider
    url: https://tushare.pro/document/1?doc_id=40
    :return:
    '''
    print('tushare_spider: start')

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

