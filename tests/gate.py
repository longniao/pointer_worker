# -*- coding: utf-8 -*-

import json
from ws4py.client.threadedclient import WebSocketClient

class DummyClient(WebSocketClient):
    def opened(self):
        #self.send('{"time" : 123456, "channel" : "futures.tickers", "event": "subscribe", "payload" : ["BTC_USD","EOS_USD"]}')
        #self.send('{"time" : 123456, "channel" : "futures.trades", "event": "subscribe", "payload" : ["BTC_USD","EOS_USD"]}')
        self.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["15m", "BTC_USD"]}')
        self.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["1h", "BTC_USD"]}')
        self.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["4h", "BTC_USD"]}')
        self.send('{"time" : 123456, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["1d", "BTC_USD"]}')

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        if m.is_text:
            recvStr = m.data.decode("utf-8")
            print(type(recvStr), recvStr)
            message = json.loads(recvStr)
            print(type(message), message)
        else:
            print(type(m), m)

if __name__ == '__main__':
    try:
        remote = 'wss://fx-ws.gateio.ws/v4/ws'
        ws = DummyClient(remote, protocols=['chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()