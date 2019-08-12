# -*- coding: utf-8 -*-

import copy
from .. import trade_data
from .. import do_insert_many, do_insert_one

async def gate_parser(data):
    '''
    {"method": "depth.update", "params": [true, {"asks": [["11782.87", "0.05179279"], ["11782.9", "0.35"], ["11785.56", "0.2"], ["11785.57", "0.65"], ["11785.59", "0.41"]], "bids": [["11776", "0.0002"], ["11772.7", "0.0092"], ["11770.33", "0.43"], ["11767.53", "0.4254"], ["11767.05", "0.08221492"]]}, "BTC_USDT"], "id": null}
    {"method": "trades.update", "params": ["BTC_USDT", [{"id": 185077997, "time": 1565346272.4163539, "price": "11782.9", "amount": "0.0424", "type": "buy"}]], "id": null}
    :return:
    '''
    print('gate_parser: start')
    if 'method' not in data or 'params' not in data:
        return False

    if data['method'] == 'trades.update':
        params = data['params']
        pair = params[0].lower()
        trades = params[1]
        if trades:
            data_list = []
            for trade in trades:
                data = copy.deepcopy(trade_data)
                data['ex'] = 'gate'
                data['pair'] = pair
                data['id'] = trade['id']
                data['time'] = trade['time']
                data['price'] = trade['price']
                data['amount'] = trade['amount']
                data['type'] = trade['type']
                data_list.append(data)
            # print(data_list)
            await do_insert_many(data_list)

    elif data['method'] == 'depth.update':
        print('depth.update')
    else:
        print('do nothing:', data['params'])
