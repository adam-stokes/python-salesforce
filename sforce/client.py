import requests
from requests_oauthlib import OAuth1
from urlparse import urlparse, urljoin
import os
import json
from xml.etree.ElementTree import XML, fromstring, tostring
from pprint import pprint

class SF(object):
    """ SF Client class """
    def __init__(self, api_version='27.0', sandbox=False):
        self.creds = json.load(open(os.path.join(os.path.expanduser("~"),
                                    ".sfcreds.json")))
        self.sessionId = None
        self.serverUrl = None
        self.sandbox = sandbox
        self.api_version = api_version
        if self.sandbox:
            self.api_url = "https://test.salesforce.com/services/OAuth/u/%s" % (self.api_version,)
        else:
            self.api_url = "https://login.salesforce.com/services/OAuth/u/%s" % (self.api_version,)

    # private
    def __parse_envelope(self, stanza):
        """ Parses soap envelope
        """
        _parsed = fromstring(stanza)
        return _parsed

    # public methods
    def request(self, method, endpoint):
        """ Formulates a proper request
            based on intended verb
        """
        if self.sessionId == None or self.serverUrl == None:
            return(127, "No session or endpoint found")
        headers = {'Content-Type' : 'text/xml',
                   'Authorization' :"Bearer %s" % (self.sessionId,)}
        _endpoint = urljoin(self.serverUrl, endpoint)
        if method == "GET":
            req = requests.get(_endpoint, headers=headers)
            return(0, json.loads(req.content))
        return(1, "Unknown error")

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
                self.serverUrl = "://".join((_parse_url.scheme, _parse_url.netloc))
            if item.tag == "sessionId":
                self.sessionId = item.text
        return(0, None)

# Test
if __name__=="__main__":
    sfapi = SF(True)
    ret, res = sfapi.session()
    if ret == 0:
        pprint(sfapi.sobjects())
