# -*- coding: utf-8 -*-

from flask import (
    current_app,
    request,
    jsonify
)

from . import main_blueprint, base_response


@main_blueprint.route('/pause_job', methods=['POST'])
def pause_job():
    response = base_response.copy()
    post_data = request.get_json(force=True)

    if 'id' not in post_data or not post_data['id']:
        current_app.apscheduler.pause()
    else:
        current_app.apscheduler.pause_job(post_data['id'])

    return jsonify(response)
