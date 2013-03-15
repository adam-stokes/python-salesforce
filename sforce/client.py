import requests

class SF(object):
    """ SF Client class """
    def __init__(self, client_key, token):
        self.client_key = client_key
        self.token = token

    def _call(self, method):
        """ Performs GET/POST/PATCH/PUT/DELETE
            requests
        """
        pass

    def request(self):
        """ Formulates a proper request
            based on intended verb
        """
        pass

    ####################################################
    # Methods inherited by public interfaces
    #
    # The purpose is to emulate simple SQL commands when
    # working with results.
    ####################################################
    def limit(self):
        """ Limit results returned
        """
        pass

    def filter(self):
        """ Filter query for records
        """
        pass

    def order(self):
        """ Order records ASC/DESC
        """
        pass

    def eq(self):
        """ Selects based on equality
        """
        pass

###############################################################################
# Public Interfaces
#
# Our schema is defined by the interfaces we wish to interact with.
# Each public interface should be defined in a separate module and only
# inherit the associated interface.
#
# TODO: Expose all resources from Salesforce and provide a sane set of
# defaults when working with results.
###############################################################################
class Account(SF):
    """ Provides Salesforce Account information
    """
    pass

class Case(SF):
    """ Provides Salesforce Case information
    """
    pass

class Lead(SF):
    """ Provides Salesforce Leads Information
    """
    pass


