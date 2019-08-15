# -*- coding: utf-8 -*-

import json
import gzip
from ws4py.client.threadedclient import WebSocketClient

client_id = '12312'

def decode_ws_payload(data):
    return json.loads(gzip.decompress(data).decode('utf-8'))

def encode_ws_payload(data):
    return json.dumps(data)

class DummyClient(WebSocketClient):
    def opened(self):
        self.send('{ "sub": "market.ethbtc.kline.15min", "id": "%s" }' % client_id)
        #self.send('{ "sub": "market.ethbtc.kline.60min", "id": "%s" }' % client_id)
        self.send('{ "sub": "market.ethbtc.kline.4hour", "id": "%s" }' % client_id)
        #self.send('{ "sub": "market.ethbtc.kline.1day", "id": "%s" }' % client_id)

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        m = decode_ws_payload(m)
        print(m)

if __name__ == '__main__':
    try:
        remote = 'wss://api.huobi.pro/ws'
        ws = DummyClient(remote, protocols=['chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()