# -*- coding: utf-8 -*-

from flask import Blueprint

main_blueprint = Blueprint('main', __name__)

base_response = dict(
    code=1,
    msg='success',
    data=[],
)

default_job = dict(
    id='',
    func='',
    args=dict(),
    trigger='',
)

from .add_job import *
from .job_list import *
from .pause_job import *
from .remove_job import *
from .resume_job import *
from .start_job import *
from .stop_job import *

