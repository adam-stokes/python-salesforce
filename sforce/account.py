from sforce import client
from pprint import pprint

class SFAccount(client.SF):
    def describe(self):
        """ Describe an Account object metadata
        """
        return self.request('GET',
                "/services/data/v%s/sobjects/Account/" % (self.api_version,))

    def accountById(self, id):
        """ Describe an Account by ID
        """
        return self.request('GET',
                "/services/data/v%s/sobjects/Account/%s" % (self.api_version, str(id)))
