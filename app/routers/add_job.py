# -*- coding: utf-8 -*-

import json
from flask import (
    current_app,
    jsonify,
    request
)

from . import main_blueprint, base_response
from app.tasks import ALL_JOBS


@main_blueprint.route('/add_job', methods=['POST'])
def add_job():
    response = base_response.copy()
    post_data = json.loads(request.get_data(as_text=True))

    if 'id' not in post_data or post_data['id'] not in ALL_JOBS:
        response['code'] = 0
        response['msg'] = 'job not found'
        return jsonify(response)
    if 'args' not in post_data:
        response['code'] = 0
        response['msg'] = 'args not found'
        return jsonify(response)

    job = ALL_JOBS[post_data['id']]
    if 'func' in post_data:
        del post_data['func']

    job.update(post_data)
    current_app.apscheduler.add_job(**job)

    return jsonify(response)
