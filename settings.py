# -*- coding: utf-8 -*-
"""
Settings for the hello scripts.

You most likely need to edit a few of them, e.g. API_HOST and the OAuth
credentials.
"""

# Get the OAuth credentials prior from the API, e.g.
# https://apisandbox.openbankproject.com/consumer-registration
CLIENT_KEY = 'tpxvzan1qt2xutnu0141o3dnsfni15jicyvoigi5'
CLIENT_SECRET = 'amr1ll3wgkvqijjjexgyvt34rymzbh02reacs2l2'


# URL you are redirected to when OAuth has succeeded. Doesn't need to exist for
# the example scripts.
REDIRECT_URL = 'https://www.example.com'

# API host to talk to
API_HOST = 'https://apisandbox.openbankproject.com'


# API version to use
API_VERSION = '3.0.0'

# API BASE URL
API_BASE_URL = '{}/obp/v{}'.format(API_HOST, API_VERSION)

# For the current user (hack)
API_USER_URL = '{}/obp/v{}/users/current'.format(API_HOST, API_VERSION)

# For initial testing, you might want to get some sample data:
# https://raw.githubusercontent.com/OpenBankProject/OBP-API/develop/src/main/scala/code/api/sandbox/example_data/example_import.json
# The account data below was taken from there

# My bank we want to send money from
MY_BANK = 'gh.29.uk'
# My account is picked automatically at the moment
# MY_ACCOUNT = ''

# The counterparty we want to send money to

COUNTERPARTY_BANK = 'gh.29.uk'
COUNTERPARTY_ACCOUNT_ID = '851273ba-90d5-43d7-bb31-ea8eba5903c7'

# Currency used for payment
PAYMENT_CURRENCY = 'EUR'

# Payment value to transfer; values < 100 will not be challenged
PAYMENT_VALUE = '0.01'

# Payment description
PAYMENT_DESCRIPTION = 'Hello Payments v1.4!'
