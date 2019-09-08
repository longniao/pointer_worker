# -*- coding: utf-8 -*-

import importlib
from flask import (
    current_app,
    jsonify,
    request
)

from . import main_blueprint, base_response, default_job


@main_blueprint.route('/add_job', methods=['POST'])
def add_job():
    response = base_response.copy()
    post_data = request.get_json(force=True)

    if 'func' not in post_data or not post_data['func'] or 'trigger' not in post_data or not post_data['trigger']:
        response['code'] = 0
        response['msg'] = 'params missed'
        return jsonify(response)

    job = default_job.copy()
    job.update(post_data)

    full_path   = 'app.tasks.' + job['func']
    path_array  = full_path.split('.')
    func_path   = '.'.join(path_array[:-1])
    func_method = path_array[-1:][0]
    func_module = importlib.import_module(func_path)

    job['func'] = getattr(func_module, func_method)
    if not job['id']:
        job['id'] = full_path
    print(job)

    current_app.apscheduler.add_job(**job)

    return jsonify(response)
