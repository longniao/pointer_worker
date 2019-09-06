# -*- coding: utf-8 -*-

import json
import arrow
import traceback
from urllib.request import urlopen, Request
from app.models.market.kline import Kline


class FeixiaohaoClient(object):

    def start(self, start_date, end_date):
        '''
        开始抓取
        :param start_date:
        :param end_date:
        :return:
        '''
        url = 'https://dncapi.bqiapp.com/api/v3/coin/history?coincode=bitcoin&begintime=%s&endtime=%s&page=1&per_page=1000&webp=1' % (
            start_date, end_date)
        return self.crawl_data(url)

    def crawl_data(self, url):
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


def collect(start_date=None, end_date=None):
    '''
    feixiaohao spider
    :return:
    {
        "func":"spider.feixiaohao_spider.collect",
        "args": ["20130101", "20200101"],
        "trigger": "date",
        "run_date":"2019-09-06 15:39:40"
    }
    '''
    if not end_date:
        end_date = arrow.now().format('YYYYMMDD')
    if not start_date:
        start_date = arrow.now().shift(days=-7).format('YYYYMMDD')

    client = FeixiaohaoClient()
    start_time = arrow.get(str(start_date), 'YYYYMMDD')
    end_time = arrow.get(str(end_date), 'YYYYMMDD')

    while start_time.year < end_time.year:
        start_time_span = start_time.span("year")

        begintime = start_time_span[0].format('YYYYMMDD')
        endtime = start_time_span[1].format('YYYYMMDD')
        print(begintime, endtime)
        client.start(begintime, endtime)

        # 开始时间增加一年
        start_time = start_time.shift(years=1)

    # 抓取当年的数据
    begintime = start_time.format('YYYYMMDD')
    endtime = end_time.format('YYYYMMDD')
    print(begintime, endtime)
    client.start(begintime, endtime)


if __name__ == '__main__':
    try:
        collect()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
