# -*- coding: utf-8 -*-

from app.library.wsclient import DummyClient

class DummyClient(WebSocketClient):
    def opened(self):
        #self.send('{"id":12312,"method":"server.ping","params":[]}')
        #self.send('{"id":12312, "method":"server.time", "params":[]}')
        #self.send('{"id":12312, "method":"ticker.query", "params":["BTC_USDT", 86400]}')
        #self.send('{"id":12312, "method":"ticker.subscribe", "params":["BTC_USDT"]}')
        #self.send('{"id":12312, "method":"ticker.unsubscribe", "params":[]}')
        #self.send('{"id":12312, "method":"trades.query", "params":["BTC_USDT", 2, 7177813]}')
        #self.send('{"id":12312, "method":"trades.subscribe", "params":["BTC_USDT", "EOS_USDT"]}')
        #self.send('{"id":12312, "method":"depth.query", "params":["BTC_USDT", 5, "0.0001"]}')
        self.send('{"id":12312, "method":"depth.subscribe", "params":["BTC_USDT", 5, "0.0001"]}')
        #self.send('{"id":12312, "method":"depth.unsubscribe", "params":[]}')
        #self.send('{"id":12312, "method":"kline.query", "params":["BTC_USDT", 1, 1516951219, 1800]}')
        #self.send('{"id":12312, "method":"kline.subscribe", "params":["BTC_USDT", 1800]}')
        #self.send('{"id":12312, "method":"kline.unsubscribe", "params":[]}')

        #self.send('{"id":956988,"method":"depth.subscribe","params":["BTC_USDT",30,"0.01"]}')
        #self.send('{"id":956988,"method":"trades.subscribe","params":["BTC_USDT"]}')

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        print(m)

if __name__ == '__main__':
    try:
        remote = 'wss://webws.gateio.live/v3/?v=972062'
        remote = 'wss://ws.gate.io/v3/'
        remote = 'wss://ws.gateio.ws/v3/'
        ws = DummyClient(remote, protocols=['chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()