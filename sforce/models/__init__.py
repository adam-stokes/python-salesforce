from sforce import client
class Schema(client.SF):
    """ Class definition for overrides in models
    """
    def describe(self):
        """ Describe object method
        """
        pass
    def get(self, id):
        """ Get object by ID
        """
        pass

