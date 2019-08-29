# -*- coding: utf-8 -*-

import json
import asyncio
import logging
import aiohttp
import traceback
from datetime import datetime

from pointer_spider.feixiaohao.parser import feixiaohao_parser


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def feixiaohao_spider():
    '''
    feixiaohao spider
    url: https://dncapi.bqiapp.com/api/v3/coin/history?coincode=bitcoin&begintime=20130301&endtime=20140301&page=1&per_page=1000&webp=1
    :return:
    '''
    print('feixiaohao_spider: start')

    async with aiohttp.ClientSession() as session:

        for year in range(2013, 2020):
            begintime = '%s0101' % year
            endtime = '%s0101' % (year + 1)

            url = 'https://dncapi.bqiapp.com/api/v3/coin/history?coincode=bitcoin&begintime=%s&endtime=%s&page=1&per_page=1000&webp=1' % (begintime, endtime)
            print(begintime, endtime, url)

            data = await fetch(session, url)
            if isinstance(data, str):
                data = json.loads(data)
            await feixiaohao_parser(data)

            print('{time}-Client receive.'.format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


if __name__ == '__main__':
    count = 0
    try:
        asyncio.get_event_loop().run_until_complete(feixiaohao_spider())
        print('try')
    except KeyboardInterrupt as exc:
        print('KeyboardInterrupt')
        logging.info('Quit.')
    except Exception as e:
        traceback.print_exc()
        print("Exception", e)



