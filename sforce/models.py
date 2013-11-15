from sforce import COMMONS as c
from sforce.client import sf_service_path, sf_request
from urllib.parse import urlencode

"""
Example account sosql query:
  'SELECT Id, CaseNumber, Subject '\
  'FROM Case '\
  'WHERE AccountId=\'%s\'' % (str(id),)

Example case sosql query:
  'SELECT Id, CommentBody, CreatedDate, IsPublished '\
  'FROM CaseComment '\
  'WHERE ParentId=\'%s\'' % (str(id),)

Example case comments sosql query:
  'SELECT Id, CommentBody, CreatedDate, IsPublished '\
  'FROM CaseComment '\
  'WHERE ParentId=\'%s\'' % (str(id),)

"""

class SObj(object):
    """ Encapsulate sobjects """
    def __init__(self, sobject=None, filter_=None, limit=None, commons=None):
        """ initialize sobject

        :param sobject: Salesforce object
        :param filter_: Query filter for object
        :param limit: Set max limit results
        :param commons: Application common attributes
        """
        self.sobject = sobject
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

    def query(self, q):
        """ query soql

        :param q: sosql query statement
        """
        _q = {'q': q}
        enc_q = urlencode(_q)
        munge_query = ''.join(('?',enc_q))
        ret, res = sf_request(self.c, 'GET', sf_service_path(self.c,
                                                             'query',
                                                             munge_query))
        return (ret, res)

    def select(self, *args):
        """ argument list of select items to return in sosql

        :param args: List of arguments to pass to sosql select statement
        """
        return "SELECT %s" % (",".join(args),)

    def from(self, *args):
        """ argument list of from item to apply in sosql

        :param args: List of table arguments to apply in sosql
        """
        return "FROM %s" % (",".join(args),)

    def where(self, clause):
        """ sosql where clause

        :param clause: a sosql WHERE statement
        """
        return "WHERE %s" % (str(clause),)

    def get(self, id):
        """ get a resource by ID

        :param id: Salesforce resource ID
        :param name: Name of sobject
        """

        return sf_request(self.c, 'GET', sf_service_path(self.c,
                                                         'sobjects',
                                                         self._name,
                                                         str(id)))

    def by_id(self, id):
        """ query sobject by salesforce ID

        :param id: Salesforce resource ID
        """
        ret, res = self.get(id)
        return (ret, res)
