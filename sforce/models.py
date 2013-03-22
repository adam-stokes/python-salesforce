from sforce import COMMONS as c
from sforce.client import sf_service_path, sf_request

def sf_sobjects(c):
    """ Returns available sobjects for defined salesforce version
    """
    return sf_request(c, 'GET', c['services']['sobjects'])

def sf_obj_describe(c, name):
    """ Describe a service object metadata
        :param name: Name of sobject to describe
    """
    return sf_request(c, 'GET', sf_service_path(c,
                                                'sobjects',
                                                name))

def sf_obj_get(c, id, name):
    """ get a resource by ID

        :param id: Salesforce resource ID
        :param name: Name of sobject
    """
    return sf_request(c, 'GET', sf_service_path(c,
                                                'sobjects',
                                                name,
                                                str(id)))

def sf_obj_update(c, id, **kwds):
    """ Update resource ID using proper dictionary of available keys
        from a returned resource

        :param id: Salesforce resource ID
        :param kwds: Field names, values to update
    """
    pass
