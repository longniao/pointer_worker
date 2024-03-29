# -*- coding: utf-8 -*-

from flask import (
    jsonify
)

from app.models.scheduler.job import Job
from . import main_blueprint, base_response


@main_blueprint.route('/job_list', methods=['GET'])
def job_list():
    response = base_response.copy()

    response['data'] = Job.get_list()

    return jsonify(response)
