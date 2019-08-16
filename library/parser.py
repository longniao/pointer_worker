# -*- coding: utf-8 -*-

import traceback
import logging
from configparser import ConfigParser
import ast

configParser = ConfigParser()

class Parser(object):

    _config = dict()

    def load(self, config_file=None):
        '''
        load config data from config file
        :param config_file:
        :return:
        '''
        if not config_file:
            raise Exception('10100', 'Error config file')

        configParser.read(config_file, encoding='UTF-8')
        self.assemble()

    def parse(self, section, item):
        '''
        parse config
        :param section:
        :param item:
        :return:
        '''
        try:
            value = configParser.get(section, item)
            value = ast.literal_eval(value)

            if section in self._config:
                self._config[section][item] = value
            else:
                self._config[section] = {item:value}

        except Exception as e:
            logging.error(traceback.format_exc())


    def assemble(self):
        '''
        assemble config
        :return:
        '''
        if configParser.sections():
            for section in configParser.sections():
                options = configParser.options(section)
                if options:
                    for option in options:
                        self.parse(section, option)

    @property
    def config(self):
        return self._config
