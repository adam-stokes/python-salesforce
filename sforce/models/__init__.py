import os
from pprint import pprint
from sforce import client

class Schema(client.SF):
    """ Class definition for overrides in models
    """
    service_name = None

    @classmethod
    def name(class_):
        """ Returns the services's name as a string. This should return a
            capitalize string.
        """
        if class_.service_name:
            return class_.service_name
        return class_.__name__.capitalize()

    # public interfaces
    def sobjects(self):
        """ Returns available sobjects for defined salesforce version
        """
        return self.request('GET', self.services['sobjects'])

    def describe(self):
        """ Describe a service object metadata
        """
        pprint(self.service('sobjects', self.name()))
        return self.request('GET', self.service('sobjects', self.name()))

    def get(self, id):
        """ get a resource by ID

            :param id: Salesforce resource ID
        """
        return self.request('GET',
                "/services/data/v%s/sobjects/%s/%s" % (self.api_version,
                                                       class_.name(),
                                                       str(id)))
    def update(self, id, **kwds):
        """ Update resource ID using proper dictionary of available keys
            from a returned resource

            :param id: Salesforce resource ID
            :param kwds: Field names, values to update
        """
        pass
