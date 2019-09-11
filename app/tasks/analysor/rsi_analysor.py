# -*- coding: utf-8 -*-

import arrow
import pandas as pd
from app.models.market import ALL_CONTRACTS, ALL_FREQS, ALL_EXS
from app.models.market.kline import Kline
from app.models.indicator.rsi import Rsi as RsiModel
from app.indicators.talib import RSI


class RsiAnalysor(object):

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
        print('rsi analyze: start')
        df = pd.DataFrame((data_list))
        df.sort_values(by="time", inplace=True)
        df['rsi'] = RSI(df)
        # print(df)
        for index, row in df.iterrows():
            if 'rsi' in row and row['rsi']:
                data = dict(
                    ex=row['ex'].lower(),
                    contract=row['contract'].lower(),
                    freq=row['freq'],
                    time=arrow.get(row['time']).datetime,
                    rsi=row['rsi'],
                )
                # print(data)
                RsiModel.insert_data(data)

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
        analysor = RsiAnalysor()
        analysor.start(limit)
    except Exception as e:
        print('Exception:',  str(e))


if __name__ == '__main__':
    try:
        do_analyze()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
