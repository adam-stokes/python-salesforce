from pprint import pprint
from requests_oauthlib import OAuth1
from urlparse import urlparse, urljoin
from xml.etree.ElementTree import XML, fromstring, tostring
import json
import os
import requests

class SF(object):
    """ SF Client class """

    def __init__(self, api_version='27.0', sandbox=False):
        self.creds = json.load(open(os.path.join(os.path.expanduser("~"),
                                    ".sfcreds.json")))
        self.commons = {
            'services': None,
            'sessionId': None,
            'serverUrl': None,
            'sandbox': sandbox,
            'api_version': api_version
        }
        if self.commons['sandbox']:
            self.api_url = "https://test.salesforce.com/services/OAuth/u/%s" % (self.commons['api_version'],)
        else:
            self.api_url = "https://login.salesforce.com/services/OAuth/u/%s" % (self.commons['api_version'],)

    # private
    def __set_available_services(self):
        """ Sets available services
        """
        ret, res = self.request('GET',
                  "/services/data/v%s" % (self.commons['api_version'],))
        if ret == 0:
            self.commons['services'] = res

    def __parse_envelope(self, stanza):
        """ Parses soap envelope
        """
        _parsed = fromstring(stanza)
        return _parsed

    # public methods
    def service(self, name, *args):
        """ Builds service URL
            :param name: Name of service (i.e 'sobjects')
            :param **args: Arguments appended to service url
        """
        pprint(self.commons['services'])
        _args = "/".join(args)
        return "/".join((self.commons['services'][name], _args))

    def request(self, method, endpoint):
        """ Formulates a proper request
            based on intended verb
        """
        if self.commons['sessionId'] == None or self.commons['serverUrl'] == None:
            return(127, "No session or endpoint found")
        headers = {'Content-Type' : 'text/xml',
                   'Authorization' :"Bearer %s" % (self.commons['sessionId'],)}
        _endpoint = urljoin(self.commons['serverUrl'], endpoint)
        if method == "GET":
            req = requests.get(_endpoint, headers=headers)
            return(0, json.loads(req.content))
        return(1, "Unknown error")

    @property
    def session(self):
        """ Entry point to accessing Salesforce API.
            This method is required in order to perform requests again the REST
            interface
        """
        oauth = OAuth1(os.environ["SFKEY"],
                       client_secret=os.environ["SFSECRET"],
                       resource_owner_key=self.creds['oauth_token'],
                       resource_owner_secret=self.creds['oauth_token_secret'])

        # Returns xml response giving us our api url and sessionId
        r = requests.post(url=self.api_url, auth=oauth)
        for item in self.__parse_envelope(r.content):
            if item.tag == "serverUrl":
                _parse_url = urlparse(item.text)
                self.commons['serverUrl'] = "://".join((_parse_url.scheme,
                                             _parse_url.netloc))
            if item.tag == "sessionId":
                self.commons['sessionId'] = item.text
        # Initialize list of services available
        self.__set_available_services()

# Test
if __name__=="__main__":
    sfapi = SF(sandbox=True)
    sfapi.session
    pprint(sfapi.commons)
