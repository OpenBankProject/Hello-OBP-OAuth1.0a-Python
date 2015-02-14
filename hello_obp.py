# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
# oauth flow in simple words: http://pyoauth.readthedocs.org/en/latest/guides/oauth1.html

client_key = "youcustomerkey"
client_secret = "youcustomersecret"

base_url = "https://ulsterbank.openbankproject.com"
request_token_url = base_url + "/oauth/initiate"
authorization_base_url = base_url + "/oauth/authorize"
access_token_url = base_url + "/oauth/token"

openbank = OAuth1Session(client_key, client_secret=client_secret, callback_uri='http://127.0.0.1/cb')

openbank.fetch_request_token(request_token_url)

authorization_url = openbank.authorization_url(authorization_base_url)
print 'Please go here and authorize, '
print authorization_url

redirect_response = raw_input('Paste the full redirect URL here:')
openbank.parse_authorization_response(redirect_response)

openbank.fetch_access_token(access_token_url)

#get accounts for a specific bank
our_bank = 'ulster-ni'
print "Available accounts"
r = openbank.get(u"{}/obp/v1.2.1/banks/{}/accounts/private".format(base_url, our_bank))

accounts = r.json()['accounts']
for a in accounts:
    print a['id']

#just picking first account
our_account = accounts[0]['id']

print "Get owner transactions"
r = openbank.get(u"{}/obp/v1.2.1/banks/ulster-ni/accounts/{}/owner/transactions".format(base_url,
    our_account), headers= {'obp_limit': '25'})
transactions = r.json()['transactions']
print "Got {} transactions".format(len(transactions))

print "Transfer some money"
send_to = {"bank": "ulster-ni", "account": "current13"}
payload = '{"account_id": "' + send_to['account'] +'", "bank_id": "' + send_to['bank'] + '", "amount": "10" }'
headers = {'content-type': 'application/json'}
r = openbank.post(u"{}/obp/v1.2.1/banks/{}/accounts/{}/owner/transactions".format(base_url,
    our_bank, our_account), data=payload, headers=headers)
print r
print r.json()

