# -*- coding: utf-8 -*-

import json
import urllib.error
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

def get_http(domain: str, path: str, port: Optional[int] = None) -> bytes:
    if not isinstance(domain, str):
        errors.type_error(f"Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`")
    if not isinstance(path, str):
        errors.type_error(f"Parameter path must be of type `str`, but got value {path} of type `{type(path).__name__}`")
    if not isinstance(port, (int, type(None))):
        errors.type_error(f"Parameter port must be of type `Optional[int]`, but got value {port} of type `{type(port).__name__}`")

    if port is None:
        port = 80

    url = f"http://{domain}:{port}/{path}"
    try:
        req = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        raise errors.ResponseFail(e.code, e.reason)

    return req.read()

def get_https(domain: str, path: str, port: Optional[int] = None, verify: bool = True) -> bytes:
    if not isinstance(domain, str):
        errors.type_error(f"Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`")
    if not isinstance(path, str):
        errors.type_error(f"Parameter path must be of type `str`, but got value {path} of type `{type(path).__name__}`")
    if not isinstance(port, (int, type(None))):
        errors.type_error(f"Parameter port must be of type `Optional[int]`, but got value {port} of type `{type(port).__name__}`")
    if not isinstance(verify, bool):
        errors.type_error(f"Parameter verify must be of type `bool`, but got value {verify} of type `{type(verify).__name__}`")

    if port is None:
        port = 443

    if verify == False:
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

    url = f"https://{domain}:{port}/{path}"
    try:
        req = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        raise errors.ResponseFail(e.code, e.reason)

    return req.read()


def post(protocal: _Protocol, domain: str, path: str, header: dict, body: dict, port: Optional[int] = None) -> dict:
    if not isinstance(protocal, _Protocol):
        errors.type_error(f"Parameter protocal must be of type `_Protocol`, but got value {protocal} of type `{type(protocal).__name__}`")
    if not isinstance(domain, str):
        errors.type_error(f"Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`")
    if not isinstance(path, str):
        errors.type_error(f"Parameter path must be of type `str`, but got value {path} of type `{type(path).__name__}`")
    if not isinstance(header, dict):
        errors.type_error(f"Parameter header must be of type `dict`, but got value {header} of type `{type(header).__name__}`")
    if not isinstance(body, dict):
        errors.type_error(f"Parameter body must be of type `dict`, but got value {body} of type `{type(body).__name__}`")
    if not isinstance(port, int):
        errors.type_error(f"Parameter port must be of type `int`, but got value {port} of type `{type(port).__name__}`")

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
