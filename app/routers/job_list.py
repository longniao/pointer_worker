# -*- coding: utf-8 -*-

import json
from flask import (
    jsonify,
    request
)

from . import main_blueprint


@main_blueprint.route('/job_list', methods=['GET'])
def job_list():
    data = json.loads(request.get_data(as_text=True))
    for key, value in data.items():
        if value == '':
            data[key] = 0
    for key, value in data.items():
        if type(value) == str and value != 'i':
            data[key] = float(value)

    return jsonify(data)
