# -*- coding: utf-8 -*-

import arrow
from app.model.market import ALL_CONTRACTS, ALL_FREQS, ALL_EXS
from app.models.market.kline import Kline

class TdAnalysor(object):

    def start(self):
        '''
        开始分析
        :return:
        '''
        for ex in ALL_EXS:
            for freq in ALL_FREQS:
                for contract in ALL_CONTRACTS:
                    try:
                        Kline.get_within(ex=ex, contract=contract, freq=freq, limit=39)
                        self.parser_data(message)
                    except Exception as e:
                        print(e, "parse failed.")
                    except:
                        print("parse failed.")

    def parser_data(self, data):
        '''
        {"time":1565775111,"channel":"futures.trades","event":"update","error":null,"result":[{"size":-1464,"id":5349902,"create_time":1565775111,"price":"10483","contract":"BTC_USD"},{"size":-2000,"id":5349903,"create_time":1565775111,"price":"10483","contract":"BTC_USD"}]}
        {"time":1565775111,"channel":"futures.tickers","event":"update","error":null,"result":[{"contract":"BTC_USD","last":"10483","change_percentage":"-7.24","funding_rate":"0.000641","mark_price":"10474.95","index_price":"10469.51","total_size":"19461274","volume_24h":"99692397","quanto_base_rate":"","volume_24h_usd":"99692397","volume_24h_btc":"9522","funding_rate_indicative":"0.0001"}]}
        :return:
        '''
        print('gate parser: start')
        if 'channel' not in data or 'event' not in data or 'result' not in data:
            return False

        if data['event'] == 'update' and not data['error']:

            timestamp = data['time']
            result = data['result']

            # K线
            if data['channel'] == 'futures.candlesticks':

                if result:
                    for row in result:
                        contract_arr = row['n'].split('_', 1)
                        contract = GATE_CONTRACT_DICT.get(contract_arr[1])
                        freq = contract_arr[0].lower()

                        # 入库
                        data = dict(
                            ex='gate',
                            contract=contract,
                            freq=freq,
                            time=arrow.get(row['t']).datetime,
                            open=row['o'],
                            high=row['h'],
                            low=row['l'],
                            close=row['c'],
                            volume=row['v'],
                        )
                        Kline.insert_data(data)

            else:
                print('do nothing:', result)


def collect():
    '''
    gate spider
    url: https://gateio.co/docs/futures/ws/index.html
    :return:
    '''
    try:
        remote = 'wss://fx-ws.gateio.ws/v4/ws'
        ws = GateClient(remote, protocols=['chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()



if __name__ == '__main__':
    try:
        collect()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
