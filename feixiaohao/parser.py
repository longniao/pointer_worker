# -*- coding: utf-8 -*-

from pointer_spider.db import *
from ..models.kline import Kline


async def feixiaohao_parser(data):
    '''
    {"tickertime":"2015-01-01T00:00:00","openprice":314.079010010000,"closeprice":315.032012939000,"high":315.838989258000,"low":313.565002441000,"marketcap":4309551126.0,"vol":7860650.0,"changerate":0.3}
    :return:
    '''
    print('feixiaohao_parser: start')
    if data['code'] != 200:
        return False

    data_list = data['data']['list']
    if data_list:
        for row in data_list:
            row['ex'] = 'all'
            row['contract'] = 'btc_usd'
            row['range'] = '1d'
            row['time'] = row['tickertime']
            row['open'] = row['openprice']
            row['close'] = row['closeprice']
            row['high'] = row['high']
            row['low'] = row['low']
            row['volume'] = row['vol']

            new_data = Kline.format(row)

            # 检测，防止重复插入
            filter = {
                'ex': new_data['ex'],
                'contract': new_data['contract'],
                'range': new_data['range'],
                'time': new_data['time'],
            }
            result = await do_find_one(Kline, filter)
            if not result:
                await do_insert_one(Kline, new_data)
            else:
                for k in filter.keys():
                    del new_data[k]

                await do_update_one(Kline, filter, new_data)

    else:
        print('do nothing:', data_list)
