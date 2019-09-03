#!/usr/bin/env python3

import os
import redis
import subprocess

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from rq import Connection, Queue, Worker
from werkzeug.security import generate_password_hash

from app import create_app, db
from config import Config, config_env

app = create_app(config_env)
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.option(
    '-n',
    '--number-users',
    default=10,
    type=int,
    help='Number of each model type to create',
    dest='number_users')
def add_fake_data(number_users):
    """
    Adds fake data to the database.
    """
    User.generate_fake(count=number_users)


@manager.command
def setup_tasks():
    """Runs the set-up needed for local development."""
    '''
    # 10秒执行一次
    {
        "func":"spider.gate_spider.collect",
        "args":[],
        "trigger": "interval",
        "seconds": 15
    }
    # 一次性执行
    {
        "id":"collect_kline",
        "args":[
            "huobi",
            "btcusdt",
            "60min"
            ],
        "trigger":"date",
        "run_date":"2019-08-30 19:06:40"
    }
    '''
    default_jobs = [
        {
            "id":"collect_gate",
            "args":[],
            "trigger": "interval",
            "minutes": 5
        },
        {
            "id": "collect_huobi",
            "args": [],
            "trigger": "interval",
            "minutes": 5
        },
    ]


@manager.command
def run_worker():
    """Initializes a slim rq task queue."""
    listen = ['default']
    redis_connection = redis.from_url(app.config['RQ_REDIS_URL'])
    with Connection(redis_connection):
        worker = Worker(map(Queue, listen))
        worker.work()


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


if __name__ == '__main__':
    manager.run()

