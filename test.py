# -*- coding: utf-8 -*-

import os
import sys
import logging
import asyncio

sys.path.insert(0, '..')
os.environ.setdefault('conf', './__conf/dev.conf')

from pointer_spider.huobi.parser import huobi_parser


async def test_huobi():

    data = {'ch': 'market.btcusdt.kline.60min', 'ts': 1565922917816,
            'tick': {'id': 1565920800, 'open': 0.018117, 'close': 0.018054, 'low': 0.018026, 'high': 0.01812,
                     'amount': 1829.8435, 'vol': 33.0590645023, 'count': 763}}

    await huobi_parser(data)


if __name__ == '__main__':
    try:
        print('start test...')
        #asyncio.get_event_loop().run_until_complete(test_huobi())
    except KeyboardInterrupt as exc:
        print('KeyboardInterrupt')
        logging.info('Quit.')
    except Exception as e:
        print(e, "Try again.")

