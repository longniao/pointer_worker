# -*- coding: utf-8 -*-

import arrow
import pandas as pd
from app.models.market import ALL_CONTRACTS, ALL_FREQS, ALL_EXS
from app.models.market.kline import Kline

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
                        data_list = Kline.get_within(ex=ex, contract=contract, freq=freq, limit=limit)
                        self.analyze_data(data_list)
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
        print(df)


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
