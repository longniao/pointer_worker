# -*- coding: utf-8 -*-

import arrow
import pandas as pd
from app.models.market import ALL_CONTRACTS, ALL_FREQS, ALL_EXS
from app.models.market.kline import Kline
from app.models.indicator.td import Td as TdModel
from app.indicators.technology.trend import TD, TD_COUNT


class TdAnalysor(object):

    def start(self, limit=50):
        '''
        开始分析
        :return:
        '''
        for ex in ALL_EXS:
            for freq in ALL_FREQS:
                for contract in ALL_CONTRACTS:
                    try:
                        data_list = Kline.get_within(ex=ex, contract=contract, freq=freq, order='-time', limit=limit)
                        if data_list:
                            self.analyze_data(data_list)
                        else:
                            print('empty data:', ex, contract, freq)
                    except Exception as e:
                        print(e, "parse failed.")
                    except:
                        print("parse failed.")

    def analyze_data(self, data_list):
        '''
        分析数据
        :param data_list:
        :return:
        '''
        print('analyze_data: start')
        df = pd.DataFrame((data_list))
        df.sort_values(by="time", inplace=True)
        df['td_count'] = TD(df)
        df['td_close'] = TD_COUNT(df, column='close')
        df['td_high'] = TD_COUNT(df, column='high')
        df['td_low'] = TD_COUNT(df, column='low')

        for index, row in df[13:].iterrows():
            data = dict(
                ex=row['ex'].lower(),
                contract=row['contract'].lower(),
                freq=row['freq'],
                time=arrow.get(row['time']).datetime,
                td_count=row['td_count'],
                td_high=row['td_high'],
                td_low=row['td_low'],
                td_close=row['td_close'],
            )
            # print(data)
            TdModel.insert_data(data)

        return True


def do_analyze(limit=50):
    '''
    :return:
    {
        "func":"analysor.td_analysor.do_analyze",
        "args": [50],
        "trigger": "date",
        "run_date":"2019-09-06 15:39:40"
    }
    '''
    try:
        analysor = TdAnalysor()
        analysor.start(limit)
    except Exception as e:
        print('Exception:',  str(e))


if __name__ == '__main__':
    try:
        do_analyze()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
