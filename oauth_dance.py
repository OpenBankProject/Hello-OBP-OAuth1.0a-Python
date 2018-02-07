# -*- coding: utf-8 -*-

"""
Handles the OAuth dance with the OpenBankProject API

It will retrieve an authorisation URL and then ask you to access it (e.g. via
web browser). Unless you have authenticated already, you will have to login to
the API and will be redirected to the callback URL (as provided in settings).
Most likely, this will result in a 404 (if you use a browser), but that does
not matter. Just paste that redirect URL into the console.

OAuth flow in simple words:
http://pyoauth.readthedocs.org/en/latest/guides/oauth1.html
"""

from requests_oauthlib import OAuth1Session
from six.moves import input

from settings import CLIENT_KEY, CLIENT_SECRET, REDIRECT_URL, API_HOST


OAUTH_BASE = '{}/oauth'.format(API_HOST)


def get_api():
    """Initiates the OAuth authorisation returns an API session object"""
    request_token_url = '{}/initiate'.format(OAUTH_BASE)
    authorization_url = '{}/authorize'.format(OAUTH_BASE)
    access_token_url = '{}/token'.format(OAUTH_BASE)

    # initiate Oauth by fetching request token
    api = OAuth1Session(
        CLIENT_KEY, client_secret=CLIENT_SECRET, callback_uri=REDIRECT_URL)
    api.fetch_request_token(request_token_url)

    # ask user to visit authorization URL and paste response
    authorization_url = api.authorization_url(authorization_url)
    print('Please visit this URL and authenticate/authorise:')
    print(authorization_url)
    redirect_response = input('Paste the full redirect URL here: ')

    # parse authorization response (contains callback_uri) and access token
    api.parse_authorization_response(redirect_response.strip())
    api.fetch_access_token(access_token_url)
    return api
