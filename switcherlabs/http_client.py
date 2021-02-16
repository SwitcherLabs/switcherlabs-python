from __future__ import absolute_import, division, print_function

import json
import warnings
import threading
import switcherlabs

try:
    import urllib.request
except ImportError:
    pass

try:
    import requests
except ImportError:
    requests = None


def new_http_client(*args, **kwargs):
    if requests:
        impl = RequestsClient
    else:
        impl = UrllibClient
        warnings.warn(
            "Warning: the SwitcherLabs library is falling back to urllib "
            "because requests is not installed. urllib SSL implementation "
            "doesn't verify server certificates. For improved security, we "
            "suggest installing requests."
        )

    return impl(*args, **kwargs)


class HTTPClient(object):
    def __init__(self):
        self._thread_local = threading.local()

    def request(self, method, url, headers, post_data=None):
        raise NotImplementedError(
            "HTTPClient subclasses must implement `request`"
        )

    def close(self):
        raise NotImplementedError(
            "HTTPClient subclasses must implement `close`"
        )


class RequestsClient(HTTPClient):
    name = "requests"

    def __init__(self, **kwargs):
        super(RequestsClient, self).__init__(**kwargs)

    def request(self, method, url, headers):
        if getattr(self._thread_local, "session", None) is None:
            self._thread_local.session = requests.Session()

        url = switcherlabs.api_base + url

        response = self._thread_local.session.request(
            method,
            url=url,
            headers=headers,
            timeout=60,
        )

        return response.json()

    def close(self):
        if getattr(self._thread_local, "session", None) is not None:
            self._thread_local.session.close()


class UrllibClient(HTTPClient):
    name = "urllib.request"

    def __init__(self, **kwargs):
        super(UrllibClient, self).__init__(**kwargs)

    def request(self, method, url, headers):
        url = switcherlabs.api_base + url
        req = urllib.request.Request(url, None, headers)

        response = urllib.request.urlopen(req)

        return json.loads(response.read())

    def close(self):
        pass
