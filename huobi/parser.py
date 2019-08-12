# -*- coding: utf-8 -*-

import copy
from .. import trade_data
from .. import do_insert_many, do_insert_one

trade_pair = {
    'btcusdt': 'btc_usdt',
    'eosusdt': 'eos_usdt',
}

action_list = ['trade', 'depth']

async def huobi_parser(data):
    '''
    {'ch': 'market.btcusdt.trade.detail', 'ts': 1565367413854, 'tick': {'id': 102028992266, 'ts': 1565367413799, 'data': [{'id': 10202899226643868708445, 'ts': 1565367413799, 'amount': 0.002074, 'price': 11799.9, 'direction': 'sell'}]}}
    :return:
    '''
    print('huobi_parser: start')
    if 'ch' not in data or 'tick' not in data:
        return False

    chs = data['ch'].split('.')
    action = chs[2]
    pair = trade_pair.get(chs[1])
    if not pair:
        return False

    if action in action_list:
        tick = data['tick']
        trades = tick['data']
        if trades:
            data_list = []
            for trade in trades:
                data = copy.deepcopy(trade_data)
                data['ex'] = 'huobi'
                data['pair'] = pair
                data['id'] = str(trade['id'])
                data['time'] = trade['ts']
                data['price'] = trade['price']
                data['amount'] = trade['amount']
                data['type'] = trade['direction']
                data_list.append(data)
            # print(data_list)
            await do_insert_many('trade', data_list)

    else:
        print('do nothing:', data)
