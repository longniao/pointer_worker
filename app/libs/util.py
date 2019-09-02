# -*- coding: utf-8 -*-

import gzip
import json


def decode_ws_payload(m):
    if m.is_text:
        recvStr = m.data.decode("utf-8")
        return json.loads(recvStr)
    else:
        return m

def encode_ws_payload(data):
    return json.dumps(data)


