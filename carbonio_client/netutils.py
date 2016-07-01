import httplib2
import json
import urlparse

########################################################################################################################
# curl functionality
########################################################################################################################

def get_url_json(url, headers=None, timeout=None, retries=0, keyfile=None, certfile=None, ca_certs=None):
    return fetch_url_json(url, method="GET", headers=headers, timeout=timeout, retries=retries,
                          keyfile=keyfile, certfile=certfile, ca_certs=ca_certs)

########################################################################################################################
def post_url_json(url, data, headers=None, timeout=None, retries=0, keyfile=None, certfile=None,
                  ca_certs=None):
    return fetch_url_json(url, method="POST", data=data, headers=headers, timeout=timeout, retries=retries,
                          keyfile=keyfile, certfile=certfile, ca_certs=ca_certs)

########################################################################################################################
def fetch_url_json(url, method=None, data=None, headers=None, timeout=None, retries=None, keyfile=None, certfile=None,
                   ca_certs=None):
    if not headers:
        headers = {}
    headers["Content-Type"] = "application/json"
    if data and isinstance(data, dict):
        data = json.dumps(data)
    result = fetch_url(url, method=method, data=data, headers=headers, timeout=timeout, retries=retries,
                       keyfile=keyfile, certfile=certfile, ca_certs=ca_certs)
    if result and not isinstance(result, bool):
        return json.loads(result)
    else:
        return result

########################################################################################################################
def fetch_url(url, method=None, data=None, headers=None, timeout=None, retries=None, keyfile=None, certfile=None,
              ca_certs=None):
    http = httplib2.Http(timeout=timeout, ca_certs=ca_certs)

    if keyfile:
        http.add_certificate(keyfile, certfile, urlparse.urlparse(url).netloc)

    retries = retries or 0
    _response = None
    _content = None
    if data and not isinstance(data, str):
        data = str(data)
    while retries >= 0 and (_response is None or _response["status"] != "200"):
        try:
            retries -= 1
            _response, _content = http.request(url, method=method or "GET", body=data, headers=headers)
        except Exception,e:
            if retries < 0:
                raise
    if _response is None or "status" not in _response:
        raise FetchUrlError("Error: Response is empty: %s" % _content)
    if _response["status"] != "200":
        raise FetchUrlError("Error (%s): %s" % (_response["status"], _content),
                            status_code=int(_response["status"]))
    if _content:
        return _content
    else:
        return True

########################################################################################################################



class FetchUrlError(Exception):
    def __init__(self, msg, status_code=None):
        Exception.__init__(self, msg)
        self._status_code = status_code

    @property
    def status_code(self):
        return self._status_code

