# -*- coding: utf-8 -*-

from config import config
from flask import Flask
from flask_apscheduler import APScheduler
from flask_babel import lazy_gettext as _
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

# 全局变量
db = MongoEngine()
scheduler = APScheduler()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = _('Please log in to access this page.')

def create_app(config_name):
    '''
    创建APP
    :param config_name:
    :return:
    '''
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)
    login_manager.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    from app.routers import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
