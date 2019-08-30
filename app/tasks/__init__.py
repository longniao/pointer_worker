# -*- coding: utf-8 -*-

from .market.coinbar import search_coinbar


ALL_JOBS = {
    'search_coinbar': {
        'id': 'search_coinbar',
        'func': search_coinbar,
        'args': '',
        'trigger': 'interval',
        'seconds': 2
    }
}


