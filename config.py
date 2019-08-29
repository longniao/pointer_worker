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
    DEBUG           = parser.config['app']['debug']
    TESTING         = parser.config['app']['testing']
    BCRYPT_LEVEL    = parser.config['app']['bcrypt_level']
    APP_NAME        = parser.config['app']['app_name']
    SECRET_KEY      = parser.config['app']['secret_key']
    WTF_CSRF_ENABLED    = parser.config['app']['wtf_csrf_enabled']

    # mongodb settings
    MONGODB_SETTINGS = parser.config['mongodb']['mongodb_settings']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN TESTING MODE.  YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    SSL_DISABLE = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert Config.SECRET_KEY, 'SECRET_KEY IS NOT SET!'


class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig
}

config_env = os.getenv('CONFIG_ENV', 'default')