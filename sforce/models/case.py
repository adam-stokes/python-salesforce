from sforce.models import Schema

class SFCase(Schema):
    def describe(self):
        """ Describe an Case object metadata
        """
        return self.request('GET',
                "/services/data/v%s/sobjects/Case/describe" % (self.api_version,))
