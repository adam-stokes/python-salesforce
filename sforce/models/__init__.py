import os
from pprint import pprint

class Schema(object):
    """ Class definition for overrides in models
    """
    service_name = None

    def __init__(self, commons):
        self.commons = commons
        self.commons['service_models'] = {}

    @classmethod
    def name(class_):
        """ Returns the services's name as a string. This should return a
            capitalize string.
        """
        if class_.service_name:
            return class_.service_name
        return class_.__name__.capitalize()

def register_model(model):
    base = model.__name__ 
    class Model(base):
        # public interfaces
        def sobjects(self):
            """ Returns available sobjects for defined salesforce version
            """
            return self.request('GET', self.commons['services']['sobjects'])

        def describe(self):
            """ Describe a service object metadata
            """
            pprint(self.service('sobjects', self.name()))
            return self.request('GET', self.service('sobjects', self.name()))

        def get(self, id):
            """ get a resource by ID

                :param id: Salesforce resource ID
            """
            return self.request('GET', self.service('sobjects',
                                                    self.name(),
                                                    str(id)))

        def update(self, id, **kwds):
            """ Update resource ID using proper dictionary of available keys
                from a returned resource

                :param id: Salesforce resource ID
                :param kwds: Field names, values to update
            """
            pass
    return Model(model)

