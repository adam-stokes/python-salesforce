from sforce.models import Schema

class SFAccount(Schema):
    def describe(self):
        """ Describe an Account object metadata
        """
        return self.request('GET',
                "/services/data/v%s/sobjects/Account/" % (self.api_version,))

    def get(self, id):
        """ get an Account by ID
        """
        return self.request('GET',
                "/services/data/v%s/sobjects/Account/%s" % (self.api_version, str(id)))
