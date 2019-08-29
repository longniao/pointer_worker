# -*- coding: utf-8 -*-

from flask import Blueprint

job_blueprint = Blueprint('job', __name__, url_prefix='/')


from .login import *
from .logout import *
from .register import *
from .reset_password import *

