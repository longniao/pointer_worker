# -*- coding: utf-8 -*-

from flask import (
    current_app,
    jsonify
)

from . import main_blueprint, base_response


@main_blueprint.route('/start_job', methods=['POST'])
def start_job():
    response = base_response.copy()

    current_app.apscheduler.start()

    return jsonify(response)
