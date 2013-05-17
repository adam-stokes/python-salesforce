from sforce import COMMONS as c
from sforce.client import sf_service_path, sf_request
import urllib

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
        return (ret, res)

    def _get(self, id):
        """ get a resource by ID

            :param id: Salesforce resource ID
            :param name: Name of sobject
        """

        ret, res = sf_request(self.c, 'GET', sf_service_path(self.c,
                                                             'sobjects',
                                                             self._name,
                                                             str(id)))
        return (ret, res)

    def query(self, q):
        """ query soql
        """
        _q = {'q': q}
        enc_q = urllib.urlencode(_q)
        munge_query = ''.join(('?',enc_q))
        ret, res = sf_request(self.c, 'GET', sf_service_path(self.c,
                                                             'query',
                                                             munge_query))
        return (ret, res)

    def by_id(self, id):
        """ Stub for searching sobject by parentid/id
        """
        pass

    def by_name(self, name):
        """ Stub for searching by name value
        """
        pass

    def all(self, **kwds):
        """ Stub for all records filtered or not
        """
        pass

class Account(Base):
    def __cases(self, id):
        """ Pull associated cases for AccountId
        """
        return self.query('SELECT Id, CaseNumber, Subject '\
                          'FROM Case '\
                          'WHERE AccountId=\'%s\'' % (str(id),))

    def by_name(self, name):
        """ Fuzzy search by account name
        """
        return self.query('SELECT Id, AnnualRevenue, Name, '\
                          'Phone, Rating, TickerSymbol, Type '\
                          'FROM Account '\
                          'WHERE Name like \'%%%s%%\'' % (name,))

    def by_id(self, id, include_cases=False):
        ret, acct = self._get(id)
        if ret == 0 and include_cases:
            ret, cases = self.__cases(id)
            if ret == 0:
                acct.Cases = cases
        return (ret, acct)

class Case(Base):
    def __comments(self, id):
        """ Aggregate comments for cases retrieved
        """
        return self.query('SELECT Id, CommentBody, CreatedDate, IsPublished '\
                          'FROM CaseComment '\
                          'WHERE ParentId=\'%s\'' % (str(id),))

    def by_id(self, id, include_comments=False):
        ret, case = self._get(id)
        if ret == 0 and include_comments:
            ret, comments = self.__comments(id)
            case['Comments'] = comments
        return (ret, case)
        

class Asset(Base):
    def by_id(self, id):
        ret, acct = self._get(id)
        if ret == 0:
            return (ret, acct)
