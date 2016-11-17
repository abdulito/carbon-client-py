__author__ = 'abdul'

from endpoint import Endpoint

from utils import dict_deep_merge
import urllib

import requests
import ssl
import json
import logging

from requests_toolbelt import SSLAdapter
import requests.packages.urllib3.connection
import socket
import time

# bind HTTPError as requests HTTPError
from requests import HTTPError as HTTPError

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
        self.persist_session = True
        # setup authenticator
        if "authentication" in self.default_options:
            self._setup_authentication(self.default_options["authentication"])

    ####################################################################################################################
    @property
    def url(self):
        return self._url

    ####################################################################################################################
    def session(self):

        if not self.persist_session:
            return self._new_session()
        else:
            if self._session is None:
                self._session = self._new_session()
            return self._session

    ####################################################################################################################
    def _new_session(self):
        session = requests.Session()
        if self.default_options and "keyfile" in self.default_options:
            session.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1))

        return session

    ####################################################################################################################
    # CLIENT METHODS
    ####################################################################################################################
    def request_endpoint(self, endpoint, method, body=None, options=None):
        options = self._apply_default_options(options)
        start_time = time.time()
        try:
            return self.do_request_endpoint(endpoint, method, body=body, options=options)
        except:
            raise
        finally:
            elapsed = time.time() - start_time
            logger.info("CarbonClient: %s %s finished in %.3f seconds" % (method, endpoint.full_url, elapsed))

    ####################################################################################################################
    def do_request_endpoint(self, endpoint, method, body=None, options=None):
        method_func = getattr(self.session(), method.lower())

        params = options and options.get("params")
        timeout = options.get("timeout") or 10
        url = endpoint.full_url
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

        response = method_func(url, params=params, data=body, headers=headers, timeout=timeout,
                               verify=ca_certs, cert=cert)
        if response.status_code < 400:
            return response
        else:
            raise HTTPError("Error (%s): %s" % (response.status_code, response.text), response=response)

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



