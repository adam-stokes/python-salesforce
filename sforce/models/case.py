from sforce.models import Schema

class Case(Schema):

    service_name = "Case" 

    def describe(self):
        """ Describe an Case object metadata
        """
        return self.request('GET',
                "/services/data/v%s/sobjects/Case/describe" % (self.api_version,))
