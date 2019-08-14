# -*- coding: utf-8 -*-

from ..db import do_insert_many
from ..models.trade import Trade
from ..models.ticker import Ticker

async def gate_parser(data):
    '''
    {"time":1565775111,"channel":"futures.trades","event":"update","error":null,"result":[{"size":-1464,"id":5349902,"create_time":1565775111,"price":"10483","contract":"BTC_USD"},{"size":-2000,"id":5349903,"create_time":1565775111,"price":"10483","contract":"BTC_USD"}]}
    {"time":1565775111,"channel":"futures.tickers","event":"update","error":null,"result":[{"contract":"BTC_USD","last":"10483","change_percentage":"-7.24","funding_rate":"0.000641","mark_price":"10474.95","index_price":"10469.51","total_size":"19461274","volume_24h":"99692397","quanto_base_rate":"","volume_24h_usd":"99692397","volume_24h_btc":"9522","funding_rate_indicative":"0.0001"}]}
    :return:
    '''
    print('gate_parser: start')
    if 'channel' not in data or 'event' not in data or 'result' not in data:
        return False

    if data['event'] == 'update' and not data['error']:

        timestamp = data['time']
        result = data['result']
        data_list = []

        # 行情
        if data['channel'] == 'futures.tickers':
            if result:
                for row in result:
                    row['ex'] = 'gate'
                    row['time'] = timestamp
                    tmp = Ticker.format(row)
                    data_list.append(tmp)

                await do_insert_many(Ticker, data_list)

        # 实时交易
        elif data['channel'] == 'futures.trades':

            if result:
                for row in result:
                    row['ex'] = 'gate'
                    row['time'] = row['create_time']
                    row['amount'] = row['size']
                    row['type'] = ''
                    tmp = Trade.format(row)
                    data_list.append(tmp)

                await do_insert_many(Trade, data_list)

        else:
            print('do nothing:', result)
