# -*- coding: utf-8 -*-

import time
import json
from ws4py.client.threadedclient import WebSocketClient

class GateClient(WebSocketClient):
    def opened(self):
        t = int(time.time())
        # 客户端给服务端发送消息
        # 行情
        # self.send('{"time" : %s, "channel" : "futures.tickers", "event": "subscribe", "payload" : ["BTC_USD","EOS_USD"]}' % t)
        # 实时交易
        # self.send('{"time" : %s, "channel" : "futures.trades", "event": "subscribe", "payload" : ["BTC_USD","EOS_USD"]}' % t)
        # 深度
        # self.send('{"time" : %s, "channel" : "futures.order_book", "event": "subscribe", "payload" : ["BTC_USD", "20", "0"]}' % t)
        # 蜡烛图/K线
        # self.send('{"time" : %s, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["10s", "BTC_USD"]}' % t)
        self.send('{"time" : %s, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["15m", "BTC_USD"]}' % t)
        self.send('{"time" : %s, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["1h", "BTC_USD"]}' % t)
        self.send('{"time" : %s, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["4h", "BTC_USD"]}' % t)
        self.send('{"time" : %s, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["1d", "BTC_USD"]}' % t)
        self.send('{"time" : %s, "channel" : "futures.candlesticks", "event": "subscribe", "payload" : ["7d", "BTC_USD"]}' % t)

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
        ws = GateClient(remote, protocols=['chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()