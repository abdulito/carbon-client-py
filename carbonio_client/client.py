__author__ = 'abdul'

from endpoint import Endpoint
from netutils import fetch_url_json, FetchUrlError
from utils import dict_deep_merge
import urllib

import requests
import ssl
import json
import logging

from requests_toolbelt import SSLAdapter
import requests.packages.urllib3.connection
import socket
########################################################################################################################
# LOGGER
########################################################################################################################

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

########################################################################################################################
# Defaulting SO_KEEPALIVE for all http connections
requests.packages.urllib3.connection.HTTPConnection.default_socket_options.extend([
    (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
])

########################################################################################################################
# Generic Carbon IO Client
########################################################################################################################


class CarbonIOClient(Endpoint):

    ####################################################################################################################
    def __init__(self, url, options=None):
        Endpoint.__init__(self, None)
        self._url = url
        self._client = self
        self.default_options = options or {}
        self._session = None
        # setup authenticator
        if "authentication" in self.default_options:
            self._setup_authentication(self.default_options["authentication"])

    ####################################################################################################################
    @property
    def url(self):
        return self._url

    def session(self):
        if self._session is None:
            self._session = requests.Session()
            if self.default_options and "keyfile" in self.default_options:
                self._session.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1))

        return self._session

    ####################################################################################################################
    # CLIENT METHODS
    ####################################################################################################################
    def request_endpoint(self, endpoint, method, body=None, options=None):
        options = self._apply_default_options(options)
        #return send_request(endpoint.full_url, method=method, body=body, options=options)
        return self.do_request_endpoint(endpoint, method, body=body, options=options)
    ####################################################################################################################
    def do_request_endpoint(self, endpoint, method, body=None, options=None):
        method_func = getattr(self.session(), method.lower())

        params = options and options.get("params")
        timeout = options.get("timeout") or 10
        url = endpoint.full_url
        url = append_params_to_url(url, params)

        headers = options and options.get("headers")
        headers = headers or {}
        headers["Content-Type"] = "application/json"
        keyfile = options and options.get("keyfile")
        certfile = options and options.get("certfile")
        ca_certs = options and options.get("ca_certs")
        cert = None
        if keyfile:
            cert = (certfile, keyfile)

        if body and isinstance(body, dict):
            body = json.dumps(body)

        response = method_func(url, data=body, headers=headers, timeout=timeout, verify=ca_certs, cert=cert)
        if response.status_code < 400:
            try:
                return response.json()
            except Exception, ex:
                logger.error("Failed to parse response to json. Raw response:\n****%s\n******" % response.text)
                raise
        else:
            raise FetchUrlError("Error (%s): %s" % (response.status_code, response.text),
                                status_code=response.status_code)

    ####################################################################################################################
    def _setup_authentication(self, authentication):
        if authentication["type"] == "api-key":
            self._setup_api_key_authentication(authentication)

    ####################################################################################################################
    def _setup_api_key_authentication(self, authentication):
        api_key_parameter_name = authentication.get("apiKeyParameterName") or "API_KEY"
        api_key_location = authentication.get("apiKeyLocation") or "header"

        if api_key_location == "header":
            if not self.default_options.get("headers"):
                self.default_options["headers"] = {}

            self.default_options["headers"][api_key_parameter_name] = authentication["apiKey"]
        elif api_key_location == "query":
            if not self.default_options.get("params"):
                self.default_options["params"] = {}

            self.default_options["params"][api_key_parameter_name] = authentication["apiKey"]
        else:
            raise Exception("Unknown apiKeyLocation '" + api_key_location + "'")


    ####################################################################################################################
    def _apply_default_options(self, options):
        options = options or {}
        if self.default_options:
            return dict_deep_merge(options, self.default_options.copy())
        else:
            return options


########################################################################################################################
# HELPERS
########################################################################################################################

def send_request(url, method=None, body=None, options=None):
    params = options and options.get("params")
    headers = options and options.get("headers")
    keyfile = options and options.get("keyfile")
    certfile = options and options.get("certfile")
    ca_certs = options and options.get("ca_certs")
    timeout = options.get("timeout") or 10
    url = append_params_to_url(url, params)
    return fetch_url_json(url=url, method=method, data=body, headers=headers, timeout=timeout, keyfile=keyfile,
                          certfile=certfile, ca_certs=ca_certs)

########################################################################################################################
def append_params_to_url(url, params):
    if params:
        url += "?"
        count = 0
        for name, val in params.items():
            if val is None:
                val = ""
            if count > 0:
                url += "&"
            url += "%s=%s" % (name, urllib.quote(val))
            count += 1
    return url

########################################################################################################################


###############################################################################
# CarbonClientError
###############################################################################
class CarbonIOClientError(Exception):
    pass



