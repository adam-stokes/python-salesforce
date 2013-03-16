import requests

class SF(object):
    """ SF Client class """
    def __init__(self, client_key, token):
        self.client_key = client_key
        self.token = token

    def _call(self):
        """ Performs GET/POST/PATCH/PUT/DELETE
            requests
        """
        pass

    def request(self, method, query):
        """ Formulates a proper request
            based on intended verb
        """
        pass

