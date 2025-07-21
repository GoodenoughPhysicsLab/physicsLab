# -*- coding: utf-8 -*-

import json
import urllib.error
import urllib.request
from physicsLab import errors
from physicsLab._typing import Optional


def get_http(domain: str, path: str, port: Optional[int] = None) -> bytes:
    if not isinstance(domain, str):
        errors.type_error(
            f"Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`"
        )
    if not isinstance(path, str):
        errors.type_error(
            f"Parameter path must be of type `str`, but got value {path} of type `{type(path).__name__}`"
        )
    if not isinstance(port, (int, type(None))):
        errors.type_error(
            f"Parameter port must be of type `Optional[int]`, but got value {port} of type `{type(port).__name__}`"
        )

    if port is None:
        port = 80

    url = f"http://{domain}:{port}/{path}"
    try:
        req = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        raise errors.ResponseFail(e.code, e.reason) from e

    return req.read()


def get_https(
    domain: str, path: str, port: Optional[int] = None, verify: bool = True
) -> bytes:
    if not isinstance(domain, str):
        errors.type_error(
            f"Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`"
        )
    if not isinstance(path, str):
        errors.type_error(
            f"Parameter path must be of type `str`, but got value {path} of type `{type(path).__name__}`"
        )
    if not isinstance(port, (int, type(None))):
        errors.type_error(
            f"Parameter port must be of type `Optional[int]`, but got value {port} of type `{type(port).__name__}`"
        )
    if not isinstance(verify, bool):
        errors.type_error(
            f"Parameter verify must be of type `bool`, but got value {verify} of type `{type(verify).__name__}`"
        )

    if port is None:
        port = 443

    if verify == False:
        import ssl

        ssl._create_default_https_context = ssl._create_unverified_context

    url = f"https://{domain}:{port}/{path}"
    try:
        req = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        raise errors.ResponseFail(e.code, e.reason) from e

    return req.read()


def post_http(
    domain: str, path: str, header: dict, body: bytes, port: Optional[int] = None
) -> dict:
    if not isinstance(domain, str):
        errors.type_error(
            f"Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`"
        )
    if not isinstance(path, str):
        errors.type_error(
            f"Parameter path must be of type `str`, but got value {path} of type `{type(path).__name__}`"
        )
    if not isinstance(header, dict):
        errors.type_error(
            f"Parameter header must be of type `dict`, but got value {header} of type `{type(header).__name__}`"
        )
    if not isinstance(body, (bytes, dict)):
        errors.type_error(
            f"Parameter body must be of type `bytes` or `dict`, but got value {body} of type `{type(body).__name__}`"
        )
    if not isinstance(port, (int, type(None))):
        errors.type_error(
            f"Parameter port must be of type `Optional[int]`, but got value {port} of type `{type(port).__name__}`"
        )

    if port is None:
        port = 80
      
    if isinstance(body, dict):
        final_body = json.dumps(body).encode("utf-8")
    else:
        final_body = body

    url = f"http://{domain}:{port}/{path}"
    req = urllib.request.Request(url, data=final_body, method="POST")
    req.headers = header

    with urllib.request.urlopen(req) as response:
        if response.getcode() != 200:
            raise errors.ResponseFail(response.getcode(), response.reason)
        if response.info().get('Content-Encoding') == 'gzip':
            import gzip
            content = gzip.decompress(response.read())
        else:
            content = response.read()
        return json.loads(content)


def post_https(
    domain: str,
    path: str,
    header: dict,
    body: bytes,
    port: Optional[int] = None,
    verify: bool = True,
) -> dict:
    if not isinstance(domain, str):
        errors.type_error(
            f"Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`"
        )
    if not isinstance(path, str):
        errors.type_error(
            f"Parameter path must be of type `str`, but got value {path} of type `{type(path).__name__}`"
        )
    if not isinstance(header, dict):
        errors.type_error(
            f"Parameter header must be of type `dict`, but got value {header} of type `{type(header).__name__}`"
        )
    if not isinstance(body, (bytes, dict)):
        errors.type_error(
            f"Parameter body must be of type `bytes` or `dict`, but got value {body} of type `{type(body).__name__}`"
        )
    if not isinstance(port, (int, type(None))):
        errors.type_error(
            f"Parameter port must be of type `Optional[int]`, but got value {port} of type `{type(port).__name__}`"
        )

    if port is None:
        port = 443

    if verify == False:
        import ssl

        ssl._create_default_https_context = ssl._create_unverified_context
        
    if isinstance(body, dict):
        final_body = json.dumps(body).encode("utf-8")
    else:
        final_body = body

    url = f"https://{domain}:{port}/{path}"
    req = urllib.request.Request(url, data=final_body, method="POST")
    req.headers = header

    with urllib.request.urlopen(req) as response:
        if response.getcode() != 200:
            raise errors.ResponseFail(response.getcode(), response.reason)
        if response.info().get('Content-Encoding') == 'gzip':
            import gzip
            content = gzip.decompress(response.read())
        else:
            content = response.read()
        return json.loads(content)
