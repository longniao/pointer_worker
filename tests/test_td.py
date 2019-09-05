# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd

pd.set_option('display.max_rows',None)
token = '0a4672439efefb2a6cf2940cce35055e6a3f0e7d381af939768f4e9d'
ts.set_token(token)
pro = ts.pro_api()
pro = ts.pro_api(token)

df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='daily', start_date='20190101', end_date='20190901')
# df = pro.coinlist(start_date='20180101', end_date='20181231')
# df = pro.coinexchanges()
# df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='60min', start_date='20190829', end_date='20190830')
# df = pro.coincap(trade_date='20170806')
# df = pro.coincap(trade_date='20190820')
# df = pro.btc_marketcap(start_date='20130801', end_date='20190905')

df.sort_values(by="date", inplace=True)

print(df)

def TD9(df):
    """
    TD序列指标
    :param df:
    :return:
    """
    condv = (df['vol'] > 0)
    cond1 = (df['close'] > df['close'].shift(4))
    cond2 = (df['close'] < df['close'].shift(4))

    df['cond_tdb_a'] = (df.groupby((((cond1)[condv])).cumsum()).cumcount() % 13 == 0).cumsum()
    df['cond_tds_a'] = (df.groupby((((cond2)[condv])).cumsum()).cumcount() % 13 == 0).cumsum()

    df['cond_tdb_b'] = (df.groupby((((cond1)[condv])).cumsum()).cumcount() % 13 != 0).cumsum()
    df['cond_tds_b'] = (df.groupby((((cond2)[condv])).cumsum()).cumcount() % 13 != 0).cumsum()

    df['tdb_a'] = df.groupby(
        df['cond_tdb_a']
    ).cumcount()

    df['tds_a'] = df.groupby(
        df['cond_tds_a']
    ).cumcount()

    df['tdb_b'] = df.groupby(
        df['cond_tdb_b']
    ).cumcount()

    df['tds_b'] = df.groupby(
        df['cond_tds_b']
    ).cumcount()

    df['tdc'] = df['tds_a'] - df['tdb_a']
    df['tdc'] = df.apply((lambda x: x['tdb_b'] % 13 if x['tdb_b'] > 13 else x['tdc']), axis=1)
    df['tdc'] = df.apply((lambda x: (x['tds_b'] % 13) * -1 if x['tds_b'] > 13 else x['tdc']), axis=1)

    return pd.DataFrame(index=df.index, data={
        'date': df['date'],
        'open': df['open'],
        'high': df['high'],
        'low': df['low'],
        'close': df['close'],
        'td_count': df['tdc']
    })


def TD(df, sequence=13):
    """
    TD序列指标
    :param df:
    :return:
    """
    condv = (df['vol'] > 0)
    cond1 = (df['close'] > df['close'].shift(4))
    cond2 = (df['close'] < df['close'].shift(4))

    df['cond_tdb_a'] = (df.groupby((((cond1)[condv])).cumsum()).cumcount() % (sequence+1) == 0).cumsum()
    df['cond_tds_a'] = (df.groupby((((cond2)[condv])).cumsum()).cumcount() % (sequence+1) == 0).cumsum()
    df['cond_tdb_b'] = (df.groupby((((cond1)[condv])).cumsum()).cumcount() % (sequence+1) != 0).cumsum()
    df['cond_tds_b'] = (df.groupby((((cond2)[condv])).cumsum()).cumcount() % (sequence+1) != 0).cumsum()

    df['tdb_a'] = df.groupby(
        df['cond_tdb_a']
    ).cumcount()

    df['tds_a'] = df.groupby(
        df['cond_tds_a']
    ).cumcount()

    df['tdb_b'] = df.groupby(
        df['cond_tdb_b']
    ).cumcount()

    df['tds_b'] = df.groupby(
        df['cond_tds_b']
    ).cumcount()

    df['tdc'] = df['tds_a'] - df['tdb_a']
    df['tdc'] = df.apply((lambda x: x['tdb_b'] % sequence if x['tdb_b'] > sequence else x['tdc']), axis=1)
    df['tdc'] = df.apply((lambda x: (x['tds_b'] % sequence) * -1 if x['tds_b'] > sequence else x['tdc']), axis=1)

    return pd.DataFrame(index=df.index, data={
        'date': df['date'],
        'open': df['open'],
        'high': df['high'],
        'low': df['low'],
        'close': df['close'],
        'td_count': df['tdc']
    })


td_df = TD(df)

cols=['date','open','high','low','close','td_count']
td_df=td_df.ix[:,cols]

print(td_df)

if __name__ == '__main__':
    try:
        pass
    except KeyboardInterrupt:
        pass
