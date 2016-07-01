__author__ = 'abdul'

from endpoint import Endpoint
from netutils import fetch_url_json
from utils import dict_deep_merge
import urllib


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

        # setup authenticator
        if "authentication" in self.default_options:
            self._setup_authentication(self.default_options["authentication"])

    ####################################################################################################################
    @property
    def url(self):
        return self._url

    ####################################################################################################################
    # CLIENT METHODS
    ####################################################################################################################
    def request_endpoint(self, endpoint, method, body=None, options=None):
        options = self._apply_default_options(options)
        return send_request(endpoint.full_url, method=method, body=body, options=options)

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
    cacerts = options and options.get("cacerts")

    url = append_params_to_url(url, params)
    return fetch_url_json(url=url, method=method, data=body, headers=headers, timeout=10*60, keyfile=keyfile,
                          certfile=certfile, cacerts=cacerts)

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



