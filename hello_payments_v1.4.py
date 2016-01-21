# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import sys

# Note: in order to use this example, you need to have at least one account
# that you can send money from (i.e. be the owner).

# API server URL
BASE_URL = "http://127.0.0.1:8080"

# enter your api credentials here, get from BASE_URL/consumer-registration
CLIENT_KEY = 'client-key'
CLIENT_SECRET = 'client-secret'

# API server will redirect your browser to this URL, should be non-functional
# You will paste the redirect location here when running the script
CALLBACK_URI = 'http://127.0.0.1/cb'

# Our account's bank
OUR_BANK = 'our-bank-id'
# Our counterpart account id (of the same currency)
OUR_COUNTERPART = 'valid-counterpart-accountid-same-currency'
# Our currency to use
OUR_CURRENCY = 'GBP'
# Our value to transfer
OUR_VALUE = '0.01'


# You probably don't need to change those
REQUEST_TOKEN_URL = BASE_URL + "/oauth/initiate"
AUTHORIZATION_BASE_URL = BASE_URL + "/oauth/authorize"
ACCESS_TOKEN_URL = BASE_URL + "/oauth/token"



openbank = OAuth1Session(CLIENT_KEY, client_secret=CLIENT_SECRET, callback_uri=CALLBACK_URI)
openbank.fetch_request_token(REQUEST_TOKEN_URL)

authorization_url = openbank.authorization_url(AUTHORIZATION_BASE_URL)
print openbank
print 'Please go here and authorize:\n', authorization_url

redirect_response = raw_input('Paste the full redirect URL here:')
openbank.parse_authorization_response(redirect_response)
openbank.fetch_access_token(ACCESS_TOKEN_URL)

#get accounts for a specific bank
print "Private accounts"
r = openbank.get(u"{}/obp/v1.4.0/banks/{}/accounts/private".format(BASE_URL, OUR_BANK))

print r.json()

accounts = r.json()['accounts']
for a in accounts:
    print a['id']

#just picking first account
our_account = accounts[0]['id']
print "our account: {}".format(our_account)

print "Get owner transactions"
r = openbank.get(u"{}/obp/v1.4.0/banks/{}/accounts/{}/owner/transactions".format(BASE_URL,
    OUR_BANK,
    our_account), headers= {'obp_limit': '25'})
transactions = r.json()['transactions']
print "Got {} transactions".format(len(transactions))

print "Get challenge request types"
r = openbank.get(u"{}/obp/v1.4.0/banks/{}/accounts/{}/owner/transaction-request-types".format(BASE_URL,
    OUR_BANK,
    our_account))

challenge_type = r.json()[0]['value']
print challenge_type


print "Initiate transaction request"
send_to = {"bank": OUR_BANK, "account": OUR_COUNTERPART}
payload = '{"to": {"account_id": "' + send_to['account'] +'", "bank_id": "' + send_to['bank'] + \
    '"}, "value": {"currency": "' + OUR_CURRENCY + '", "amount": "' + OUR_VALUE + '"}, "description": "Description abc", "challenge_type" : "' + \
    challenge_type + '"}'
headers = {'content-type': 'application/json'}
r = openbank.post(u"{}/obp/v1.4.0/banks/{}/accounts/{}/owner/transaction-request-types/{}/transaction-requests".format(
    BASE_URL, OUR_BANK, our_account, challenge_type), data=payload, headers=headers)
initiate_response = r.json()

if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

if (initiate_response['challenge'] != None):
    #we need to answer the challenge
    challenge_query = initiate_response['challenge']['id']
    transation_req_id = initiate_response['id']['value']

    print "Challenge query is {}".format(challenge_query)
    body = '{"id": "' + challenge_query + '","answer": "123456"}'    #any number works in sandbox mode
    r = openbank.post(u"{}/obp/v1.4.0/banks/{}/accounts/{}/owner/transaction-request-types/sandbox/transaction-requests/{}/challenge".format(
        BASE_URL, OUR_BANK, our_account, transation_req_id), data=body, headers=headers
    )

    challenge_response = r.json()
    if "error" in challenge_response:
        sys.exit("Got an error: " + str(challenge_response))

    print "Transaction status: {}".format(challenge_response['status'])
    print "Transaction created: {}".format(challenge_response["transaction_ids"])
else:
    #There was no challenge, transaction was created immediately
    print "Transaction was successfully created: {}".format(initiate_response["transaction_ids"])
