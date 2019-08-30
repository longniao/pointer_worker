# -*- coding: utf-8 -*-

from .market.kline import search_kline


ALL_JOBS = {
    'search_kline': {
        'id': 'search_kline',
        'func': search_kline,
        'args': '',
        'trigger': 'interval',
        'seconds': 5
    }
}


