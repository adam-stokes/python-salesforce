from sforce import COMMONS as c
from sforce.util import Struct
from sforce.client import sf_service_path, sf_request
import yaml

class Base(object):
    def __init__(self, commons):
        self.c = commons

    @property
    def _name(self):
        """ return name of class instance
        """
        return self.__class__.__name__.capitalize()

    def sobjects(self):
        """ Returns available sobjects for defined salesforce version
        """
        return sf_request(self.c, 'GET', self.c['services']['sobjects'])

    def describe(self):
        """ Describe a service object metadata
            :param name: Name of sobject to describe
        """
        ret, res = sf_request(self.c, 'GET', sf_service_path(self.c,
                                                             'sobjects',
                                                             self._name))
        return yaml.dump(res)

    def get(self, id):
        """ get a resource by ID

            :param id: Salesforce resource ID
            :param name: Name of sobject
        """

        ret, res = sf_request(self.c, 'GET', sf_service_path(self.c,
                                                             'sobjects',
                                                             self._name,
                                                             str(id)))
        return (ret, Struct(res))

    def update(c, id, **kwds):
        """ Update resource ID using proper dictionary of available keys
        from a returned resource

        :param id: Salesforce resource ID
        :param kwds: Field names, values to update
        """
        pass

    def query(self, query):
        """ SOQL
        """
        query_str = "+".join(args)
        ret, res = sf_request(self.c, 'GET', sf_service_path(self.c,
                                                             'query',
                                                             query_str))
        return (ret, Struct(res))

class Account(Base):
    pass

class Case(Base):
    pass

class Lead(Base):
    pass

class Asset(Base):
    pass
