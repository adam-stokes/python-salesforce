from requests_oauthlib import OAuth1
from sforce import container
from urlparse import parse_qs
import requests

def request_phase(c):
    """ Perform initial OAuth Request to get a token, secret
    """
    request_url = container(c, c['request_path'])
    oauth = OAuth1(c['client_key'], 
                   client_secret=c['client_secret'],
                   callback_uri=c['callback_uri'])

    r = requests.post(url=request_url, auth=oauth)
    credentials = parse_qs(r.content)
    c['oauth_token'] = credentials.get('oauth_token')[0]
    c['oauth_token_secret'] = credentials.get('oauth_token_secret')[0]

def authorize_phase(c):
    """ Perform authorization task
        :return: authorized url
    """
    url_root = container(c, c['authorize_path'])
    url_query = "?oauth_token=%s&oauth_consumer_key=%s" % (c['oauth_token'],
                                                           c['client_key'])
    url = url_root + url_query
    return url

def access_phase(c, verifier):
    """ Access phase
    """
    access_url = container(c, c['access_path'])
    oauth = OAuth1(c['client_key'],
                   client_secret=c['client_secret'],
                   resource_owner_key=c['oauth_token'],
                   resource_owner_secret=c['oauth_token_secret'],
                   verifier=verifier)
    r = requests.post(url=access_url, auth=oauth)
    credentials = parse_qs(r.content)
    c['oauth_token'] = credentials.get('oauth_token')[0]
    c['oauth_token_secret'] = credentials.get('oauth_token_secret')[0]
