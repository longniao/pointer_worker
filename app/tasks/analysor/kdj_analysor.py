# -*- coding: utf-8 -*-

import arrow
import pandas as pd
from app.models.market import ALL_CONTRACTS, ALL_FREQS, ALL_EXS
from app.models.market.kline import Kline
from app.models.indicator.kdj import Kdj as KdjModel
from app.indicators.technology.countertrend import KDJ


class KdjAnalysor(object):

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
        df_kdj = KDJ(df)
        df = pd.concat([df, df_kdj], axis=1)

        for index, row in df[13:].iterrows():
            data = dict(
                ex=row['ex'].lower(),
                contract=row['contract'].lower(),
                freq=row['freq'],
                time=arrow.get(row['time']).datetime,
                kdj_k=row['kdj_k'],
                kdj_d=row['KDJ_D'],
                kdj_j=row['kdj_j'],
            )
            # print(data)
            KdjModel.insert_data(data)

        return True


def do_analyze(limit=50):
    '''
    :return:
    {
        "func":"analysor.kdj_analysor.do_analyze",
        "args": [50],
        "trigger": "date",
        "run_date":"2019-09-06 15:39:40"
    }
    '''
    try:
        analysor = KdjAnalysor()
        analysor.start(limit)
    except Exception as e:
        print('Exception:',  str(e))


if __name__ == '__main__':
    try:
        do_analyze()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
