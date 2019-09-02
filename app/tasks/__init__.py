# -*- coding: utf-8 -*-

from .spider.tushare_spider import collect_tushare_kline, collect_tushare_capital
from .spider.gate_spider import collect_gate
from .spider.huobi_spider import collect_huobi


ALL_JOBS = {
    'collect_tushare_kline': {
        'id': 'collect_tushare_kline',
        'func': collect_tushare_kline,
        'args': '',
        'trigger': 'interval'
    },
    'collect_tushare_capital': {
        'id': 'collect_tushare_capital',
        'func': collect_tushare_capital,
        'args': '',
        'trigger': 'interval'
    },
    'collect_gate': {
        'id': 'collect_gate',
        'func': collect_gate,
        'args': '',
        'trigger': 'interval'
    },
    'collect_huobi': {
        'id': 'collect_huobi',
        'func': collect_huobi,
        'args': '',
        'trigger': 'interval'
    },
}


