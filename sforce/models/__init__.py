import os
from sforce import client
from sforce.util import ImporterHelper, import_resource

class Schema(client.SF):
    """ Class definition for overrides in models
    """
    registered_services = []
    service_name = None

    @classmethod
    def name(class_):
        """ Returns the services's name as a string. This should return a
            capitalize string.
        """
        if class_.service_name:
            return class_.service_name
        return class_.__name__.capitalize()

    # private methods
    @property
    def __available(self):
        """ Returns available services for salesforce version
        """
        return self.request('GET',
                  "/services/data/v%s" % (self.api_version,))

    def __load(self, res_class):
        self.registered_services.append((res_class.name(),res_class))

    def __register_services(self):
        """ Registers SF Service to existing Schema
        """
        import sforce.models
        helper = ImporterHelper(sforce.models)
        resources = helper.get_modules()
        for res in resources:
            rbase, ext = os.path.splitext(res)
            res_classes = import_resource(rbase)
            for res_class in res_classes:
                self.__load(res_class)

    # services handler
    @property
    def services(self):
        """ Return list of available services
            (i.e. Account, Case, Leads)
        """
        if len(self.registered_services) < 1:
            self.__register_services()
        return self.registered_services

    # public interfaces
    def sobjects(self):
        """ Returns available sobjects for defined salesforce version
        """
        return self.request('GET',
                "/services/data/v%s/sobjects" % (self.api_version,))

    def describe(self):
        """ Describe a service object metadata
        """
        pass

    def get(self, id):
        """ Get object by ID
            This method should be overrided
        """
        pass

    def update(self, id, **kwds):
        """ Update resource ID using proper dictionary of available keys
            from a returned resource
        """
        pass
