# -*- coding: utf-8 -*-

from flask import (
    current_app,
    jsonify
)

from . import main_blueprint, base_response


@main_blueprint.route('/stop_job', methods=['POST'])
def stop_job():
    response = base_response.copy()

    current_app.apscheduler.stop()

    return jsonify(response)
