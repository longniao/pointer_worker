# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd

pd.set_option('display.max_rows',None)
token = '0a4672439efefb2a6cf2940cce35055e6a3f0e7d381af939768f4e9d'
ts.set_token(token)
pro = ts.pro_api()
pro = ts.pro_api(token)

df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='60min', start_date='20190821', end_date='20190908')
# df = pro.coinlist(start_date='20180101', end_date='20181231')
# df = pro.coinexchanges()
# df = pro.coinbar(exchange='huobi', symbol='btcusdt', freq='60min', start_date='20190829', end_date='20190830')
# df = pro.coincap(trade_date='20170806')
# df = pro.coincap(trade_date='20190820')
# df = pro.btc_marketcap(start_date='20130801', end_date='20190905')

# df.sort_values(by="date", inplace=True)



def TD(df, sequence=13):
    """
    TD序列指标: 连续9根K线的收盘价比各自前面第4根K线的收盘价 高或低。
    TD计数: 连续出现9根K线（TD结构，9根K线的收盘价都比各自前面的第4根K线收盘价高或低）之后，进行TD计数，最多计到13。
    :param df:
    :param sequence: 序列长度
    :return:
    """
    df = df.copy()
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
        'td_count': df['tdc']
    })

def TD_COUNT(df, shift=2, column='close'):
    """
    TD计数: strict 严格计数 | loose 宽松计数
    TD计数: 连续出现9根K线（TD结构，9根K线的收盘价都比各自前面的第4根K线收盘价高或低）之后，进行TD计数，最多计到13。
    TD严格计数：从第9到第13根K线，要求比各自前第2根K的最高价高 或 最低价低。
    TD宽松计数：从第9到第13根K线，要求比各自前第2根K的收盘价 高或低。

    TD序列: TD结构 + TD计数 共同构成 TD序列.
    TD组合: 比TD序列更严格的是TD组合。
    对于日K线图来说，德马克认为TD组合要比TD系列更有效一些。
    最有效的TD信号: 理想状态是， TD系列和TD组合信号发生重合，这样的信号更有效。
    TD最有效的交易信号：TD计数与TD组合发生共震时! 不同时间周期TD计数或TD组合 发生共震时!
    :param df:
    :param shift: 偏移长度
    :return:
    """
    condv = (df['vol'] > 0)
    cond1 = (df[column] > df[column].shift(shift))
    cond2 = (df[column] < df[column].shift(shift))

    df['cond_tdb_a'] = ((cond1)[condv]).cumsum()
    df['cond_tds_a'] = ((cond2)[condv]).cumsum()

    df['tdb_a'] = df.groupby(
        df['cond_tdb_a']
    ).cumcount()
    df['tds_a'] = df.groupby(
        df['cond_tds_a']
    ).cumcount()
    df['tdc'] = df['tds_a'] - df['tdb_a']

    key = 'tdc_%s' % column
    return pd.DataFrame(index=df.index, data={
        key: df['tdc']
    })

df_td = df.copy()
df_td['td_count'] = TD(df)
df_td['td_close'] = TD_COUNT(df, column='close')
df_td['td_high'] = TD_COUNT(df, column='high')
df_td['td_low'] = TD_COUNT(df, column='low')

print(df_td)



if __name__ == '__main__':
    try:
        pass
    except KeyboardInterrupt:
        pass
