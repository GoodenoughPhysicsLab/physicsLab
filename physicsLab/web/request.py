# -*- coding: utf-8 -*-

import json
import urllib.request
from enum import Enum, unique
from physicsLab import errors
from physicsLab._typing import Optional

@unique
class _Protocol(Enum):
    http = 0
    https = 1

    def __str__(self):
        return self.name

def get(protocal: _Protocol, domain: str, path: str, port: Optional[int] = None):
    ...

def post(protocal: _Protocol, domain: str, path: str, header: dict, body: dict, port: Optional[int] = None):
    if not isinstance(protocal, _Protocol):
        errors.type_error("Parameter protocal must be of type `_Protocol`, but got value {protocal} of type `{type(protocal).__name__}`")
    if not isinstance(domain, str):
        errors.type_error("Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`")

    if port is None:
        if protocal == _Protocol.https:
            port = 443
        elif protocal == _Protocol.http:
            port = 80
        else:
            errors.unreachable()

    url = f"{protocal}://{domain}:{port}/{path}"
    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.headers = header

    with urllib.request.urlopen(req) as response:
        if response.getcode() != 200:
            raise errors.ResponseFail(response.getcode(), response.reason)
        return json.loads(response.read())
