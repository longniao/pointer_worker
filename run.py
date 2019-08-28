# -*- coding: utf-8 -*-

import os
import sys
import logging
import asyncio
import subprocess

sys.path.insert(0, '..')

from pointer_spider.gate.spider import gate_spider
from pointer_spider.huobi.spider import huobi_spider


def get_argv():
    args = sys.argv[1:]
    if args == []:
        print(
'''
Usage:
  python server.py <command>
Commands:
  huobi   : huobi api
  gate    : gate api
'''
        )
    else:
        return args[0]


async def run_apider(spider=None):
    print('main: start')
    if spider == 'huobi':
        await huobi_spider()
    elif spider == 'gate':
        await gate_spider()


if __name__ == '__main__':
    spider_name = get_argv()
    if spider_name is None:
        print('please input ...')
    else:
        while True:
            try:
                print('start event_loop...')
                event_loop = asyncio.get_event_loop()
                result = event_loop.run_until_complete(run_apider(spider_name))
                # event_loop.run_forever()
            except KeyboardInterrupt as exc:
                print('KeyboardInterrupt')
                logging.info('Quit.')
                break
            except Exception as e:
                print(e, "Try again.")
                continue

