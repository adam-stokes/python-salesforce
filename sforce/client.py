import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs, urlunparse
import os
import json
from pprint import pprint

class SF(object):
    """ SF Client class """
    def __init__(self):
        self.creds = json.load(open(os.path.join(os.path.expanduser("~"), ".sfcreds.json")))
        pprint(self.creds)
        self.api_url = "https://login.salesforce.com/services/OAuth/u/27.0"

    def _call(self):
        """ Performs GET/POST/PATCH/PUT/DELETE
            requests
        """
        oauth = OAuth1(os.environ["SFKEY"],
                       client_secret=os.environ["SFSECRET"],
                       resource_owner_key=self.creds['oauth_token'],
                       resource_owner_secret=self.creds['oauth_token_secret'])
        r = requests.post(url=self.api_url, auth=oauth)
        pprint(r.content)
        credentials = parse_qs(r.content)
 
    def request(self, method, query):
        """ Formulates a proper request
            based on intended verb
        """
        pass


"""
Test caller
"""
if __name__=="__main__":
    sfapi = SF()
    sfapi._call()
