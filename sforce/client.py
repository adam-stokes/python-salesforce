import requests
from requests_oauthlib import OAuth1
from urlparse import urlparse, urljoin
import os
import json
from xml.etree.ElementTree import XML, fromstring
from pprint import pprint

class SF(object):
    """ SF Client class """
    def __init__(self, sandbox=False):
        self.creds = json.load(open(os.path.join(os.path.expanduser("~"),
                                    ".sfcreds.json")))
        self.sessionid = None
        self.serverurl = None
        self.sandbox = sandbox
        if self.sandbox:
            self.api_url = "https://test.salesforce.com/services/OAuth/u/27.0"
        else:
            self.api_url = "https://login.salesforce.com/services/OAuth/u/27.0"

    def parse_envelope(self, stanza):
        """ Parses soap envelope
        """
        _parsed = fromstring(stanza)
        return _parsed

    def session(self):
        """ Performs GET/POST/PATCH/PUT/DELETE
            requests
        """
        oauth = OAuth1(os.environ["SFKEY"],
                       client_secret=os.environ["SFSECRET"],
                       resource_owner_key=self.creds['oauth_token'],
                       resource_owner_secret=self.creds['oauth_token_secret'])
        r = requests.post(url=self.api_url, auth=oauth)
        for item in self.parse_envelope(r.content):
            if item.tag == "serverUrl":
                _parse_url = urlparse(item.text)
                self.serverurl = "://".join((_parse_url.scheme, _parse_url.netloc))
            if item.tag == "sessionId":
                self.sessionid = item.text
        return(0, None)

    def request(self, method, endpoint):
        """ Formulates a proper request
            based on intended verb
        """
        if self.sessionid == None or self.serverurl == None:
            return(127, "No session or endpoint found")
        headers = {'Content-Type' : 'text/xml',
                   'Authorization' :"Bearer %s" % (self.sessionid,)}
        _endpoint = urljoin(self.serverurl, endpoint)
        if method == "GET":
            req = requests.get(_endpoint, headers=headers)
        return(0, json.loads(req.content))

    def available(self):
        ret, resources = self.request('GET',
                "/services/data/v27.0")
        return(0, resources)

    def sobjects(self):
        ret, resources = self.request('GET',
                "/services/data/v27.0/sobjects")
        return(0, resources)


"""
Test caller
"""
if __name__=="__main__":
    sfapi = SF(True)
    ret, res = sfapi.session()
    if ret == 0:
        pprint(sfapi.available())
