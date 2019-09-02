# -*- coding: utf-8 -*-

import gzip
import json


def decode_ws_payload(m):
    if m.is_text:
        recvStr = m.data.decode("utf-8")
        return json.loads(recvStr)
    elif m.is_binary:
        recvStr = gzip.decompress(m.data)
        return json.loads(recvStr)
    else:
        return json.loads(m)


def encode_ws_payload(data):
    return json.dumps(data)


