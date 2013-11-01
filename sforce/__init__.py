__version__ = "0.2.0"
COMMONS = dict(
               api_version='27.0',
               client_key=None,
               client_secret=None,
               callback_uri=None,
               request_path="/_nc_external/system/security/oauth/RequestTokenHandler",
               authorize_path="/setup/secur/RemoteAccessAuthorizationPage.apexp",
               access_path="/_nc_external/system/security/oauth/AccessTokenHandler",
               oauth_token=None,
               oauth_token_secret=None,
               sandbox=True,
               containment=("https://test.salesforce.com",
                            "https://login.salesforce.com",),
               services=None,
               sessionId=None,
               serverUrl=None,
               api_url=None,
              )

def container(c, endpoint):
    """ Define our container (sandbox, production)
    """
    if c['sandbox']:
      return c['containment'][0] + endpoint
    return  c['containment'][1] + endpoint
