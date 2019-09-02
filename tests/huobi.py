# -*- coding: utf-8 -*-

import arrow
import json
import gzip
from ws4py.client.threadedclient import WebSocketClient

client_id = '12312'

def decode_ws_payload(data):
    return json.loads(gzip.decompress(data).decode('utf-8'))

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

    def received_message(self, message):
        try:
            data = decode_ws_payload(message)
            if 'ch' in data:
                print('parser:', data)
            elif 'ping' in data:
                self.send('{"pong": %s}' % data['ping'])
            else:
                print("continue", data)

            print('{time}-Client receive.'.format(time=arrow.now()))

        except Exception as e:
            print(e, "decode failed.")
        except:
            print("decode failed.")

if __name__ == '__main__':
    try:
        remote = 'wss://api.huobi.pro/ws'
        ws = HuobiClient(remote, protocols=['chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()

