# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session

client_key = "yourcustomerkey"
client_secret = "yourcustomersecret"

base_url = "https://apisandbox.openbankproject.com"
request_token_url = base_url + "/oauth/initiate"
authorization_base_url = base_url + "/oauth/authorize"
access_token_url = base_url + "/oauth/token"

openbank = OAuth1Session(client_key, client_secret=client_secret, callback_uri='http://127.0.0.1/cb')

openbank.fetch_request_token(request_token_url)

authorization_url = openbank.authorization_url(authorization_base_url)
print('Please go here and authorize: ', authorization_url)

redirect_response = input('Paste the full redirect URL here:')
openbank.parse_authorization_response(redirect_response)

openbank.fetch_access_token(access_token_url)

r = openbank.get(base_url + "/obp/v1.2.1/banks/testbank/accounts/private")
print(r.json())
