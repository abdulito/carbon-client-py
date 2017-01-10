__author__ = 'abdul'

import json
from utils import dict_deep_merge
########################################################################################################################
# Carbon Endpoint
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
        if self == self.client:
            return self.client.url
        else:
            return self.client.url + "/" + self.absolute_path

    ####################################################################################################################
    def get_endpoint(self, path):
        return self._do_get_get_endpoint(path)

    ####################################################################################################################
    def get_collection(self, path):
        return self._do_get_get_endpoint(path, clazz=Collection)

    def _do_get_get_endpoint(self, path, clazz=None):
        if path not in self._endpoints:
            endpoint = self._new_endpoint(path, clazz=clazz)
            self._endpoints[path] = endpoint
        return self._endpoints[path]

    ####################################################################################################################

    def get(self, params=None, options=None):
        options = options or {}
        if params:
            if options.get("params"):
                options["params"] = dict_deep_merge(options["params"], params.copy())
            else:
                options["params"] = params
        return self._client.request_endpoint(self, "GET", options=options)

    ####################################################################################################################
    def post(self, body=None, options=None):
        return self._client.request_endpoint(self, "POST", body=body, options=options)

    ####################################################################################################################
    def put(self, body=None, options=None):
        return self._client.request_endpoint(self, "PUT", body=body, options=options)

    ####################################################################################################################
    def delete(self):
        return self._client.request_endpoint(self, "DELETE")

    ####################################################################################################################
    def _new_endpoint(self, path, clazz=None):
        clazz = clazz or Endpoint
        return clazz(path, parent=self, client=self.client)


########################################################################################################################
# Collection Endpoint
########################################################################################################################


class Collection(Endpoint):

    ####################################################################################################################
    def __init__(self, path, parent=None, client=None):
        super(Collection, self).__init__(path, parent=parent, client=client)

    ####################################################################################################################
    def _object_endpoint(self, _id):
        return self.get_endpoint(str(_id))

    ####################################################################################################################
    def insert(self, obj):
        return self.post(body=obj).json()

    ####################################################################################################################
    def find(self, query=None, options=None):
        query = query or {}
        return self.get(
            params={
                "query": json.dumps(query),
                "options": options
            }
        ).json()

    ####################################################################################################################
    def delete_object(self, _id):

        return self._object_endpoint(_id).delete().json()

    ####################################################################################################################
    def find_object(self, _id):
        return self._object_endpoint(_id).get().json()

    ####################################################################################################################
    def update(self, query, obj, options=None):
        return self.put(
            body={
                "q": query,
                "o": obj
            }
        ).json()

    ####################################################################################################################
    def update_object(self, _id, obj):
        return self._object_endpoint(_id).put(
            body={
                "o": obj
            }
        ).json()