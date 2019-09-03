# -*- coding: utf-8 -*-

import json
import arrow
import traceback
from urllib.request import urlopen, Request
from app.models.market.kline import Kline


class FeixiaohaoClient(object):

    def get_data(self, url):
        try:
            request = Request(url)
            lines = urlopen(request, timeout=10).read()
            if len(lines) < 50:  # no data
                return None

            result = json.loads(lines.decode('utf-8'))
            return self.parser_data(result)
        except Exception:
            print(traceback.print_exc())

    def parser_data(self, result):
        '''
        {"openprice":9608.265871000000,"closedprice":9894.446587000000,"vol":5566067864.7092,"changecount":0.0,"changerate":2.9784845657087875144624003296,"high":9949.902048000000,"low":9599.072215000000,"high_week":10707.196360000000,"low_week":9391.474483000000,"high_month":12239.052413000000,"low_month":9391.474483000000,"high_3month":13796.489080700000,"low_3month":7571.470972090000,"high_his":20089.000000000000,"low_his":65.526000976600,"high_his_time":"2017-12-17T00:00:00","low_his_time":"2013-07-05T00:00:00","fallrate_ath":-46.84,"price":10679.711441000000,"change":286.180716000000}
        :return:
        '''
        print('feixiaohao parser: start')
        if 'data' not in result:
            return False

        if result['data']['list']:
            data_list = result['data']['list']
            for row in data_list:
                # 入库
                data = dict(
                    ex='feixiaohao',
                    contract='btc_usdt',
                    freq='1d',
                    time=arrow.get(row['tickertime']).datetime,
                    open=row['openprice'],
                    high=row['high'],
                    low=row['low'],
                    close=row['closeprice'],
                    volume=row['vol'],
                )
                # print(data)
                Kline.insert_data(data)

        else:
            print('do nothing:', result)


def collect(start, end):
    '''
    feixiaohao spider
    :return:
    '''
    client = FeixiaohaoClient()
    for year in range(start, end):
        begintime = '%s0101' % year
        endtime = '%s0101' % (year + 1)
        print(begintime, endtime)
        url = 'https://dncapi.bqiapp.com/api/v3/coin/history?coincode=bitcoin&begintime=%s&endtime=%s&page=1&per_page=1000&webp=1' % (begintime, endtime)
        client.get_data(url)


if __name__ == '__main__':
    try:
        collect()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
