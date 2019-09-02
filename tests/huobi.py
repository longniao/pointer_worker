# -*- coding: utf-8 -*-

import arrow
import json
import gzip
from ws4py.client.threadedclient import WebSocketClient

client_id = '12312'

contract_map = {
    'btcusdt': 'btc_usdt',
    'eosusdt': 'eos_usdt',
}

kline_range_map = {
    '15min': '15m',
    '60min': '1h',
    '4hour': '4h',
    '1day': '1d',
}

action_list = ['trade', 'depth']


def decode_ws_payload(m):
    if m.is_text:
        recvStr = m.data.decode("utf-8")
        return json.loads(recvStr)
    elif m.is_binary:
        recvStr = gzip.decompress(m.data)
        return json.loads(recvStr)
    else:
        return json.loads(m)

def encode_ws_payload(data):
    return json.dumps(data)

class HuobiClient(WebSocketClient):
    def opened(self):
        # 客户端给服务端发送消息
        # self.send('{"pong": %s}' % mseconds)
        # 行情
        # self.send('{ "sub": "market.btcusdt.detail", "id": "%s" }' % client_id)
        # 实时交易
        # self.send('{ "sub": "market.btcusdt.trade.detail", "id": "%s" }' % client_id)
        # 深度
        # self.send('{ "sub": "market.btcusdt.depth.step1", "id": "%s" }' % client_id)
        # 蜡烛图/K线
        self.send('{ "sub": "market.btcusdt.kline.15min", "id": "%s" }' % client_id)
        self.send('{ "sub": "market.btcusdt.kline.60min", "id": "%s" }' % client_id)
        self.send('{ "sub": "market.btcusdt.kline.4hour", "id": "%s" }' % client_id)
        self.send('{ "sub": "market.btcusdt.kline.1day", "id": "%s" }' % client_id)

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        try:
            data = decode_ws_payload(m)
            if 'ch' in data:
                self.parser_data(data)
            elif 'ping' in data:
                self.send('{"pong": %s}' % data['ping'])
            else:
                print("continue", data)

            print('{time}-Client receive.'.format(time=arrow.now()))

        except Exception as e:
            print(e, "decode failed.")
        except:
            print("decode failed.")

    def parser_data(self, data):
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
        if not contract:
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

                    print(data)

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

            print(data)

        else:
            print('do nothing:', data)


if __name__ == '__main__':
    try:
        remote = 'wss://api.huobi.pro/ws'
        ws = HuobiClient(remote, protocols=['chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()

