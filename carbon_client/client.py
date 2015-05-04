__author__ = 'abdul'

from endpoint import Endpoint
from netutils import fetch_url_json



########################################################################################################################
# Generic Carbon Client
########################################################################################################################


class CarbonClient(Endpoint):

    ####################################################################################################################
    def __init__(self, url):
        Endpoint.__init__(self, None)
        self._url = url
        self._client = self

    ####################################################################################################################
    @property
    def url(self):
        return self._url

    ####################################################################################################################
    # CLIENT METHODS
    ####################################################################################################################
    def request_endpoint(self, endpoint, method, params=None, data=None, options=None):
        return send_request(endpoint.full_url, method=method,
                            params=params, data=data, options=options)
########################################################################################################################
# HELPERS
########################################################################################################################

def send_request(url, params=None, data=None, method=None, options=None):
    url = append_params_to_url(url, params)
    return fetch_url_json(url=url, method=method, data=data)

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
class CarbonClientError(Exception):
    pass
