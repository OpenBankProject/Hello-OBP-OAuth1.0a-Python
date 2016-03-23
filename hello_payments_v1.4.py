#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script will execute a payment transation via the OpenBankProject API

Note: in order to use this example, you need to have at least one account
that you can send money from (i.e. be the owner).

Configure settings.py to suit your needs.
"""

import json
import sys

from oauth_dance import get_api
from settings import (
    API_BASE_URL,
    MY_BANK,
    COUNTERPARTY_BANK,
    COUNTERPARTY_ACCOUNT_ID,
    PAYMENT_CURRENCY,
    PAYMENT_VALUE,
    PAYMENT_DESCRIPTION,
)


URL_MY_BANK = '{}/banks/{}'.format(API_BASE_URL, MY_BANK)
URL_PRIVATE_ACCOUNTS = '{}/accounts/private'.format(URL_MY_BANK)
FMT_URL_TRANSACTIONS = '{}/accounts/{}/owner/transactions'
FMT_URL_REQUEST_TYPES = '{}/accounts/{}/owner/transaction-request-types'
FMT_URL_TRANSACTION_REQUESTS = \
    FMT_URL_REQUEST_TYPES + '/{}/transaction-requests'
FMT_URL_TRANSACTION_CHALLENGE = \
    FMT_URL_REQUEST_TYPES + '/sandbox/transaction-requests/{}/challenge'

TRANSACTIONS_LIMIT = '25'


def get_account(api):
    """Get my account (id) from the API"""
    # Print some account info
    print('Getting private accounts ...')
    response = api.get(URL_PRIVATE_ACCOUNTS)
    data = response.json()
    for account in data['accounts']:
        print(' Available account id: {}'.format(account['id']))

    # Just picking first account
    my_account = data['accounts'][0]['id']
    print("Picking account: {}".format(my_account))
    return my_account


def print_transactions(api, my_account):
    """Prints number of transactions on my account in the API"""
    url_transactions = FMT_URL_TRANSACTIONS.format(URL_MY_BANK, my_account)
    headers = {
        'obp_limit': TRANSACTIONS_LIMIT,
    }
    print("Getting transactions for my account ...")
    response = api.get(url_transactions, headers=headers)
    transactions = response.json()['transactions']
    print("Got {} transactions".format(len(transactions)))


def get_challenge_type(api, my_account):
    """Gets the challenge type to use for the payment from the API"""
    url_request_types = FMT_URL_REQUEST_TYPES.format(URL_MY_BANK, my_account)
    print("Getting challenge request types ...")
    response = api.get(url_request_types)
    challenge_type = response.json()[0]['value']
    print("Got type {}".format(challenge_type))
    return challenge_type


def initiate_transaction(api, my_account):
    """
    Initiates a transaction request on the API

    Either payment will be processed directly or a challenge is returned.
    """
    challenge_type = get_challenge_type(api, my_account)
    url_transaction_requests = FMT_URL_TRANSACTION_REQUESTS.format(
        URL_MY_BANK, my_account, challenge_type)
    data = json.dumps({
        'to': {
            'account_id': COUNTERPARTY_ACCOUNT_ID,
            'bank_id': COUNTERPARTY_BANK,
        },
        'value': {
            'currency': PAYMENT_CURRENCY,
            'amount': PAYMENT_VALUE,
        },
        'description': PAYMENT_DESCRIPTION,
        'challenge_type': challenge_type,
    })
    headers = {'content-type': 'application/json'}
    print("Initiating transaction request ...")
    response = api.post(url_transaction_requests, data=data, headers=headers)
    response = response.json()
    return response


def answer_challenge(api, my_account, challenge_query, transaction_request_id):
    """Answers the API's transaction request challenge"""
    print("Challenge query is {}".format(challenge_query))
    url_transaction_challenge = FMT_URL_TRANSACTION_CHALLENGE.format(
        URL_MY_BANK, my_account, transaction_request_id)
    data = json.dumps({
        'id': challenge_query,
        'answer': '123456',  # any number works in sandbox mode
    })
    headers = {'content-type': 'application/json'}
    print("Answering challenge ...")
    response = api.post(url_transaction_challenge, data=data, headers=headers)
    response = response.json()
    if 'error' in response:
        sys.exit('Got an error: ' + str(response))
    return response


def pay(api, my_account):
    """Handles the payment process"""
    response = initiate_transaction(api, my_account)
    if 'error' in response:
        sys.exit("Got an error: " + str(response))
    if response['challenge'] is not None:
        print('This request is challenged, you have {} attempt(s)'.format(
            response['challenge']['allowed_attempts']))
        response = answer_challenge(
            api,
            my_account,
            response['challenge']['id'],
            response['id']['value'],
        )
    print('Transaction status: {}'.format(response['status']))
    print('Created transaction id: {}'.format(response['transaction_ids']))


def hello_payment():
    """Say hello, Payment!"""
    api = get_api()
    my_account = get_account(api)
    print_transactions(api, my_account)
    pay(api, my_account)


if __name__ == '__main__':
    hello_payment()
