__author__ = 'abdul'



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
        return self._client.request_endpoint(self, "GET", params=params, options=options)

    ####################################################################################################################
    def post(self, data=None, options=None):
        return self._client.request_endpoint(self, "POST", data=data, options=options)

    ####################################################################################################################
    def put(self, data=None, options=None):
        return self._client.request_endpoint(self, "PUT", data=data, options=options)

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
    def _get_object_endpoint(self, _id):
        # TODO XXX had to pass the id as a string to deal with a bug in objectserver
        return self.get_endpoint('"%s"' % _id)

    ####################################################################################################################
    def insert(self, obj):
        return self.post(data=obj)

    ####################################################################################################################
    def find(self, query=None, options=None):
        return self.get(
            params={
                "q": query,
                "options": options
            }
        )

    ####################################################################################################################
    def remove_object(self, _id):

        return self._get_object_endpoint(_id).delete()

    ####################################################################################################################
    def get_object(self, _id):
        return self._get_object_endpoint(_id).get()

    ####################################################################################################################
    def update(self, query, obj, options=None):
        return self.put(
            data={
                "q": query,
                "o": obj
            }
        )

    ####################################################################################################################
    def update_object(self, _id, obj):
        return self._get_object_endpoint(_id).put(
            data={
                "o": obj
            }
        )