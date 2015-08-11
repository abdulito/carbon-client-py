__author__ = 'abdul'

from endpoint import Endpoint
from netutils import fetch_url_json



########################################################################################################################
# Generic Carbon IO Client
########################################################################################################################


class CarbonIOClient(Endpoint):

    ####################################################################################################################
    def __init__(self, url, auth_headers=None):
        Endpoint.__init__(self, None)
        self._url = url
        self._client = self
        self._auth_headers = auth_headers

    ####################################################################################################################
    @property
    def url(self):
        return self._url

    ####################################################################################################################
    # CLIENT METHODS
    ####################################################################################################################
    def request_endpoint(self, endpoint, method, params=None, data=None, options=None):
        return send_request(endpoint.full_url, method=method,
                            params=params, data=data, options=options,
                            headers=self._auth_headers)

########################################################################################################################
# HELPERS
########################################################################################################################

def send_request(url, params=None, data=None, method=None, headers=None, options=None):
    url = append_params_to_url(url, params)
    return fetch_url_json(url=url, method=method, data=data, headers=headers)

########################################################################################################################
def append_params_to_url(url, params):
    if params:
        url += "?"
        count = 0
        for name, val in params.items():
            if count > 0:
                url += "&"
            url += "%s=%s" % (name, val)
            count += 1
    return url

########################################################################################################################


###############################################################################
# CarbonClientError
###############################################################################
class CarbonIOClientError(Exception):
    pass
