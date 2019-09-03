# -*- coding: utf-8 -*-

from flask import (
    current_app,
    request,
    jsonify
)

from . import main_blueprint, base_response


@main_blueprint.route('/resume_job', methods=['POST'])
def resume_job():
    response = base_response.copy()
    post_data = request.get_json(force=True)

    if 'id' not in post_data or not post_data['id']:
        current_app.apscheduler.resume()
    else:
        current_app.apscheduler.resume_job(post_data['id'])

    return jsonify(response)
