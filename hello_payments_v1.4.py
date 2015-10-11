# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
# oauth flow in simple words: http://pyoauth.readthedocs.org/en/latest/guides/oauth1.html

client_key = "youcustomerkey"
client_secret = "youcustomersecret"

base_url = "https://apisandbox.openbankproject.com"
request_token_url = base_url + "/oauth/initiate"
authorization_base_url = base_url + "/oauth/authorize"
access_token_url = base_url + "/oauth/token"

openbank = OAuth1Session(client_key, client_secret=client_secret, callback_uri='http://127.0.0.1/cb')
openbank.fetch_request_token(request_token_url)

authorization_url = openbank.authorization_url(authorization_base_url)
print openbank
print 'Please go here and authorize:\n', authorization_url

redirect_response = raw_input('Paste the full redirect URL here:')
openbank.parse_authorization_response(redirect_response)
openbank.fetch_access_token(access_token_url)

#get accounts for a specific bank
our_bank = 'rbs'
print "Available accounts"
r = openbank.get(u"{}/obp/v1.4.0/banks/{}/accounts/private".format(base_url, our_bank))

print r.json()

accounts = r.json()['accounts']
for a in accounts:
    print a['id']

#just picking first account
our_account = accounts[0]['id']
print "our account: {}".format(our_account)

print "Get owner transactions"
r = openbank.get(u"{}/obp/v1.4.0/banks/{}/accounts/{}/owner/transactions".format(base_url,
    our_bank,
    our_account), headers= {'obp_limit': '25'})
transactions = r.json()['transactions']
print "Got {} transactions".format(len(transactions))

print "Get challenge request types"
r = openbank.get(u"{}/obp/v1.4.0/banks/{}/accounts/{}/owner/transaction-request-types".format(base_url,
    our_bank,
    our_account))

challenge_type = r.json()[0]['value']
print challenge_type


print "Initiate transaction request"
send_to = {"bank": our_bank, "account": "valid-counterpart-accountid-same-currency"}
payload = '{"to": {"account_id": "' + send_to['account'] +'", "bank_id": "' + send_to['bank'] + \
    '"}, "value": {"currency": "GBP", "amount": "1"}, "description": "Description abc", "challenge_type" : "' + \
    challenge_type + '"}'
headers = {'content-type': 'application/json'}
r = openbank.post(u"{}/obp/v1.4.0/banks/{}/accounts/{}/owner/transaction-request-types/sandbox/transaction-requests".format(base_url,
    our_bank, our_account), data=payload, headers=headers)
r_json = r.json()
challenge_query = r_json['challenge']['id']
transation_req_id = r_json['transactionRequestId']['value']

print "Challenge query is {}".format(challenge_query)
 #any number works in sandbox mode
body = '{"id": "' + challenge_query + '","answer": "123456"}'
r = openbank.post(u"{}/obp/v1.4.0/banks/{}/accounts/{}/owner/transaction-request-types/sandbox/transaction-requests/{}/challenge".format(base_url,
    our_bank, our_account, transation_req_id), data=body, headers=headers)

challenge_response = r.json()
print "Transaction status: {}".format(challenge_response['status'])
