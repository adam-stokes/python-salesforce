class Schema(object):
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

    def one(self):
        """ Retrieves 1 record
        """
        pass

    def all(self):
        """ Retrieves all records
        """
        pass

class Integer(Schema):
    """ Integer Type
    """
    def __call__(self, i):
        return int(i)

class String(Schema):
    """ String Type
    """
    def __call__(self, i):
        return str(i)

class Text(Schema):
    """ Text Type
    """
    def __call__(self, i):
        return str(i)

class Model(Schema):
    """ Model representation for Salesforce Resource
    """
    pass
