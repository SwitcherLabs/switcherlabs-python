from __future__ import absolute_import, division, print_function

import base64
import platform
import time

from switcherlabs import http_client, version

api_base = "https://api.switcherlabs.com"
default_http_client = None


class Client(object):
    def __init__(self,
                 api_key=None,
                 state_refresh_rate=60,
                 identity_refresh_rate=5):
        global default_http_client

        self._state_refresh_rate = state_refresh_rate
        self._identity_refresh_rate = identity_refresh_rate

        if default_http_client:
            self._client = default_http_client
        else:
            default_http_client = http_client.new_http_client()
            self._client = default_http_client

        self._api_key = api_key
        self._headers = self._make_headers()

        self._flags = {}
        self._overrides = {}
        self._identities = {}
        self._lastRefresh = 0

        self._refresh_state()

    def _make_headers(self):
        headers = {
            'Content-Type': 'application/json'
        }

        sdk_v = version.VERSION
        py_v = platform.python_version()
        user_agent = "switcherlabs-python/%s python /%s" % (sdk_v, py_v)

        headers["User-Agent"] = user_agent

        if self._api_key is not None:
            basic_auth_string = ":%s" % self._api_key
            base64_bytes = base64.b64encode(basic_auth_string.encode('ascii'))
            auth = "Basic %s" % base64_bytes.decode('ascii')
            headers["Authorization"] = auth

        return headers

    def _refresh_state(self):
        now = time.time()

        if self._lastRefresh + self._state_refresh_rate > now:
            return

        response = self._client.request(
            "GET", "/sdk/initialize", self._headers)

        self._flags = {flag['key']: flag for flag in response['flags']}
        self._overrides = {override['key']: override for override in response['overrides']}
        self._lastRefresh = now

    def _fetch_identity(self, identifier):
        now = time.time()

        if identifier in self._identities \
            and (self._identities[identifier]["fetched_at"] +
                 self._identity_refresh_rate) > now:
            return self._identities[identifier]

        response = self._client.request(
            "GET", "/sdk/identities/%s" % identifier, self._headers)

        response['fetched_at'] = now
        self._identities[identifier] = response

        return response

    def evaluate_flag(self, key, identifier=None):
        if key not in self._flags:
            raise Exception("flag requested does not exist")

        if identifier is not None:
            identity = self._fetch_identity(identifier)
            if key in identity["overrides"]:
                return identity["overrides"][key]

        self._refresh_state()

        if key in self._overrides:
            return self._overrides[key]["value"]

        return self._flags[key]["value"]
