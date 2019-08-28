# -*- coding: utf-8 -*-

import os
from kits.parser.conf import ConfParser

basedir = os.path.dirname(__file__)

config_file = os.getenv('CONFIG_FILE', '../pointer_conf/dev/spider.conf')
parser = ConfParser()
parser.load(config_file)

class Config:
    '''
    app settings
    '''
    mongodb = parser.config['mongodb']
    proxy   = parser.config['proxy']
