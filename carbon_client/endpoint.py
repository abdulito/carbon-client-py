__author__ = 'abdul'



########################################################################################################################
# Generic Carbon Client
########################################################################################################################


class Endpoint(object):

    ####################################################################################################################
    def __init__(self, path, parent=None, client=None):
        self._path = path
        self._endpoints = {}
        self._parent = parent
        self._client = client

    ####################################################################################################################
    @property
    def path(self):
        return self._path

    ####################################################################################################################
    @property
    def client(self):
        return self._client

    ####################################################################################################################
    @property
    def parent(self):
        return self._parent

    ####################################################################################################################
    @property
    def absolute_path(self):
        if self.parent and self.parent != self.client:
            return self.parent.absolute_path + "/" + self.path
        else:
            return self.path

    ####################################################################################################################
    @property
    def full_url(self):
        return self.client.url + "/" + self.absolute_path

    ####################################################################################################################

    def get_endpoint(self, path):
        if path not in self._endpoints:
            endpoint = self._new_endpoint(path)
            self._endpoints[path] = endpoint
        return self._endpoints[path]

    ####################################################################################################################

    def get(self, params=None, options=None):
        return self._client.request_endpoint(self, "GET", params=params, options=options)

    ####################################################################################################################
    def post(self, data=None, options=None):
        return self._client.request_endpoint(self, "POST", data=data, options=options)

    ####################################################################################################################
    def delete(self):
        return self._client.request_endpoint(self, "DELETE")

    ####################################################################################################################
    def _new_endpoint(self, path):
        return Endpoint(path, parent=self, client=self.client)


