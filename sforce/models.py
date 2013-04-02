from sforce import COMMONS as c
from sforce.util import Struct
from sforce.client import sf_service_path, sf_request
import urllib
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

    def _get(self, id):
        """ get a resource by ID

            :param id: Salesforce resource ID
            :param name: Name of sobject
        """

        ret, res = sf_request(self.c, 'GET', sf_service_path(self.c,
                                                             'sobjects',
                                                             self._name,
                                                             str(id)))
        return (ret, Struct(res))

    def query(self, q):
        """ query soql
        """
        _q = {'q': q}
        enc_q = urllib.urlencode(_q)
        munge_query = ''.join(('?',enc_q))
        ret, res = sf_request(self.c, 'GET', sf_service_path(self.c,
                                                             'query',
                                                             munge_query))
        return (ret, Struct(res))

    def by_id(self, id):
        """ Stub for searching sobject by parentid/id
        """
        pass

    def all(self, **kwds):
        """ Stub for all records filtered or not
        """
        pass

class Account(Base):
    def by_id(self, id):
        ret, acct = self._get(id)
        if ret == 0:
            return (ret, acct)

class Case(Base):
    def __comments(self, id):
        """ Aggregate comments for cases retrieved
        """
        return self.query('SELECT Id, CommentBody, CreatedDate, IsPublished '\
                          'FROM CaseComment '\
                          'Where ParentId=\'%s\'' % (str(id),))

    def by_id(self, id):
        ret, case = self._get(id)
        if ret == 0:
            ret, comments = self.__comments(id)
            if ret == 0:
                case.Comments = [comments]
        return (ret, case)
        

class Asset(Base):
    def by_id(self, id):
        ret, acct = self._get(id)
        if ret == 0:
            return (ret, acct)
