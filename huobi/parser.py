# -*- coding: utf-8 -*-

from ..db import do_insert_many, do_insert_one
from ..models.trade import Trade
from ..models.ticker import Ticker
from ..models.kline import Kline

contract_map = {
    'btcusdt': 'btc_usd',
    'eosusdt': 'eos_usd',
}

kline_range_map = {
    '15min': '15m',
    '60min': '1h',
    '4hour': '4h',
    '1day': '1d',
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

    contract = contract_map.get(chs[1])
    action = chs[2]
    if not pair:
        return False

    # 实时交易
    if action == 'trade':
        trades = data['tick']['data']
        if trades:
            data_list = []
            for trade in trades:
                if trade['ts'] > 9999999999:
                    trade['ts'] = trade['ts'] / 1000

                data = dict(
                    ex='huobi',
                    contract=contract,
                    id=trade['id'],
                    time=trade['ts'],
                    price=trade['price'],
                    amount=trade['amount'],
                    type=trade['direction'],
                )

                data_list.append(data)
            # print(data_list)
            await do_insert_many(Trade, data_list)

    # 深度
    elif action == 'depth':
        pass

    # K线
    elif action == 'kline':
        range = kline_range_map.get(chs[3])
        tick = data['tick']

        data = dict(
            ex='huobi',
            contract=contract,
            range=range,
            time=tick['id'],
            open=tick['open'],
            close=tick['close'],
            high=tick['high'],
            low=tick['low'],
            amount=tick['amount'],
            count=tick['count'],
            volume=tick['vol'],
        )
        await do_insert_one(Kline, data)

    else:
        print('do nothing:', data)
