from requests_oauthlib import OAuth1
from sforce import (COMMONS as c,
                    container)
from urlparse import urlparse, urljoin
from xml.etree.ElementTree import XML, fromstring, tostring
import json
import os
import requests
import sys

def sf_load_creds(c):
    """ Load sf creds
    """
    _creds_fp = None
    try:
        _creds_fp = open(os.path.join(os.path.expanduser("~"),".sfcreds.json"))
    except IOError:
        print("Cannot locate ~/.sfcreds.json; youll need to run sf-exchange-auth first.")
        sys.exit(127)

    _creds = json.load(_creds_fp)
    c['oauth_token'] = _creds['oauth_token']
    c['oauth_token_secret'] = _creds['oauth_token_secret']

def sf_api(c):
    if c['sandbox']:
        c['api_url'] = "https://test.salesforce.com/services/OAuth/u/%s"\
                % (c['api_version'],)
    else:
        c['api_url'] = "https://login.salesforce.com/services/OAuth/u/%s"\
                % (c['api_version'],)

def sf_parse_envelope(stanza):
    """ Parses soap envelope
    """
    _parsed = fromstring(stanza)
    return _parsed

def sf_services(c):
    """ Sets available services
    """
    ret, res = sf_request(c,
                          'GET',
                          "/services/data/v%s" % (c['api_version'],))
    if ret == 0:
        c['services'] = res

def sf_service_path(c, name, *args):
    """ Builds service URL
        :param name: Name of service (i.e 'sobjects')
        :param **args: Arguments appended to service url
    """
    _args = "/".join(args)
    return "/".join((c['services'][name], _args))

def sf_request(c, method, endpoint):
    """ Formulates a proper request
        based on intended verb
    """
    if c['sessionId'] == None or c['serverUrl'] == None:
        return(127, "No session or endpoint found")
    headers = {'Content-Type' : 'text/xml',
               'Authorization' :"Bearer %s" % (c['sessionId'],)}
    _endpoint = urljoin(c['serverUrl'], endpoint)
    if method == "GET":
        req = requests.get(_endpoint, headers=headers)
        return(0, json.loads(req.content))
    return(1, "Unknown error")

def sf_session(c):
    """ Entry point to accessing Salesforce API.
        This method is required in order to perform requests again the REST
        interface
    """
    oauth = OAuth1(c["client_key"],
                   client_secret=c["client_secret"],
                   resource_owner_key=c['oauth_token'],
                   resource_owner_secret=c['oauth_token_secret'])

    # Returns xml response giving us our api url and sessionId
    sf_api(c)
    r = requests.post(url=c['api_url'], auth=oauth)
    for item in sf_parse_envelope(r.content):
        if item.tag == "serverUrl":
            _parse_url = urlparse(item.text)
            c['serverUrl'] = "://".join((_parse_url.scheme,
                                         _parse_url.netloc))
        if item.tag == "sessionId":
            c['sessionId'] = item.text
    # Initialize list of services available
    sf_services(c)

# Test
if __name__=="__main__":
    c['sandbox'] = True
    c['client_key'] = os.environ['SFKEY']
    c['client_secret'] = os.environ['SFSECRET']
    # Intialize session
    sf_session(c)
