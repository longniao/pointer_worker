# -*- coding: utf-8 -*-

import arrow
from app.model.market import ALL_CONTRACTS, ALL_FREQS, ALL_EXS
from app.models.market.kline import Kline

class TdAnalysor(object):

    def start(self):
        '''
        开始分析
        :return:
        '''
        for ex in ALL_EXS:
            for freq in ALL_FREQS:
                for contract in ALL_CONTRACTS:
                    try:
                        data_list = Kline.get_within(ex=ex, contract=contract, freq=freq, limit=39)
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


def do_analyze():
    '''
    :return:
    '''
    try:
        analysor = TdAnalysor()
        analysor.start()
    except Exception as e:
        print('Exception:',  str(e))


if __name__ == '__main__':
    try:
        do_analyze()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
