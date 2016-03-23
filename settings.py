# -*- coding: utf-8 -*-
"""
Settings for the hello scripts.

You most likely need to edit a few of them, e.g. API_HOST and the OAuth
credentials.
"""

# Get the OAuth credentials prior from the API, e.g.
# https://apisandbox.openbankproject.com/consumer-registration
# OAuth data for for anil.x.d.n@example.com
CLIENT_KEY = '2na3xkig0kehgywgrdxq5aquodtq320oep2sq3zz'
CLIENT_SECRET = 'vvil0c1tkqcvzqmo22lzjzaopt1gpy3zix3vlikd'

# URL you are redirected to when OAuth has succeeded. Doesn't need to exist for
# the example scripts.
CALLBACK_URL = 'http://i_dont_exist'

# API host to talk to
API_HOST = 'http://127.0.0.1:8080'

# API version to use
API_VERSION = '1.4.0'

# API BASE URL
API_BASE_URL = '{}/obp/v{}'.format(API_HOST, API_VERSION)


# For initial testing, you might want to get some sample data:
# https://raw.githubusercontent.com/OpenBankProject/OBP-API/develop/src/main/scala/code/api/sandbox/example_data/example_import.json
# The account data below was taken from there

# My bank we want to send money from
MY_BANK = 'obp-bank-x-gh'
# My account is picked automatically at the moment
# MY_ACCOUNT = ''

# The counterparty we want to send money to

COUNTERPARTY_BANK = 'obp-bank-x-gh'
COUNTERPARTY_ACCOUNT_ID = '213527de-c423-452a-b2f8-8475e4cc2cfe'

# Currency used for payment
PAYMENT_CURRENCY = 'GBP'

# Payment value to transfer; values < 100 will not be challenged
PAYMENT_VALUE = '0.01'

# Payment description
PAYMENT_DESCRIPTION = 'Hello Payments v1.4!'



# Secret token for e.g data import
SECRET_TOKEN = 'c02964c926bd4d8d8cb513a04'
