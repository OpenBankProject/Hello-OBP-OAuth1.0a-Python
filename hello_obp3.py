# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session

client_key = "2aii20v4al12btbahozwgknr5egt0sj12xppgt31"
client_secret = "x5qdq32xlktyasl30myp2ytxkshnjoj0rrtcjaaz"

request_token_url = "https://apisandbox.openbankproject.com/oauth/initiate"
authorization_base_url = "https://apisandbox.openbankproject.com/oauth/authorize"
access_token_url = "https://apisandbox.openbankproject.com/oauth/token"

openbank = OAuth1Session(client_key, client_secret=client_secret, callback_uri='http://127.0.0.1/cb')

openbank.fetch_request_token(request_token_url)

authorization_url = openbank.authorization_url(authorization_base_url)
print('Please go here and authorize,', authorization_url)

redirect_response = input('Paste the full redirect URL here:')
openbank.parse_authorization_response(redirect_response)

openbank.fetch_access_token(access_token_url)

r = openbank.get("https://apisandbox.openbankproject.com/obp/v1.2.1/banks/rbs/accounts/private")
print(r.json())
