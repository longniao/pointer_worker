# -*- coding: utf-8 -*-

import arrow
from ws4py.client.threadedclient import WebSocketClient
from app.libs.util import decode_ws_payload
from app.models.market.kline import Kline

client_id = '12312'

HUOBI_CONTRACT_DICT = {
    'btcusdt': 'btc_usdt',
    'eosusdt': 'eos_usdt',
}

HUOBI_FREQ_DICT = {
    '15min': '15m',
    '60min': '1h',
    '4hour': '4h',
    '1day': '1d',
}


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
            data = decode_ws_payload(m)
            if 'ch' in data:
                self.parser_data(data)
            elif 'ping' in data:
                self.send('{"pong": %s}' % data['ping'])
            else:
                print("continue", data)
        except Exception as e:
            print(e, "parse failed.")
        except:
            print("parse failed.")

    def parser_data(self, data):
        '''
        {'ch': 'market.btcusdt.trade.detail', 'ts': 1565367413854, 'tick': {'id': 102028992266, 'ts': 1565367413799, 'data': [{'id': 10202899226643868708445, 'ts': 1565367413799, 'amount': 0.002074, 'price': 11799.9, 'direction': 'sell'}]}}
        :return:
        '''
        print('huobi parser: start')
        if 'ch' not in data or 'tick' not in data:
            return False

        chs = data['ch'].split('.')

        contract = HUOBI_CONTRACT_DICT.get(chs[1])
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
            freq = HUOBI_FREQ_DICT.get(chs[3])
            row = data['tick']

            # 入库
            data = dict(
                ex='huobi',
                contract=contract,
                freq=freq,
                time=arrow.get(row['id']).datetime,
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                count=row['count'],
                amount=row['amount'],
                volume=row['vol'],
            )
            Kline.insert_data(data)

        else:
            print('do nothing:', data)


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
