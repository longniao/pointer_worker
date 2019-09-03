# -*- coding: utf-8 -*-

from flask import (
    current_app,
    jsonify,
    request
)

from . import main_blueprint, base_response


@main_blueprint.route('/remove_job', methods=['POST'])
def remove_job():
    response = base_response.copy()
    post_data = request.get_json(force=True)

    if 'id' not in post_data or not post_data['id']:
        response['code'] = 0
        response['msg'] = 'params missed'
        return jsonify(response)

    current_app.apscheduler.remove_job(post_data['id'])

    return jsonify(response)
