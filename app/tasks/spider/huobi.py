# -*- coding: utf-8 -*-

import arrow
from ws4py.client.threadedclient import WebSocketClient
from app.libs.util import decode_ws_payload
from app.models.market.kline import Kline

HUOBI_CONTRACT_DICT = {
    'BTC_USD': 'btc_usdt',
}

class HuobiClient(WebSocketClient):
    def opened(self):
        #self.send('{"time" : 123456, "channel" : "futures.tickers", "event": "subscribe", "payload" : ["BTC_USD","EOS_USD"]}')
        #self.send('{"time" : 123456, "channel" : "futures.trades", "event": "subscribe", "payload" : ["BTC_USD","EOS_USD"]}')
        self.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["15m", "BTC_USD"]}')
        self.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["1h", "BTC_USD"]}')
        self.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["4h", "BTC_USD"]}')
        self.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["1d", "BTC_USD"]}')

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        message = decode_ws_payload(message)
        self.parser_data(message)

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


def collect_huobi():
    '''
    huobi spider
    url: https://huobiapi.github.io/docs/spot/v1/cn/
    :return:
    '''
    try:
        remote = 'wss://api.huobi.pro/ws'
        ws = HuobiClient(remote, protocols=['chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()



if __name__ == '__main__':
    try:
        remote = 'wss://api.huobi.pro/ws'
        ws = HuobiClient(remote, protocols=['chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
