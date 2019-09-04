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
        # 检测任务
        job = current_app.apscheduler.get_job(post_data['id'])
        if not job:
            response['code'] = 0
            response['msg'] = 'job not found'
            return jsonify(response)

        current_app.apscheduler.pause_job(post_data['id'])

    return jsonify(response)
