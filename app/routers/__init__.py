# -*- coding: utf-8 -*-

from flask import Blueprint

main_blueprint = Blueprint('main', __name__)

base_response = dict(
    code=1,
    msg='success',
    data=[],
)

from .add_job import *


