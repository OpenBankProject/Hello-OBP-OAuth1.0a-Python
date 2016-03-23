#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Imports sample data into your sandbox
"""

import random
import string

import requests

from settings import API_HOST, SECRET_TOKEN


URL_IMPORT = '{}/obp/vsandbox/v1.0/data-import?secret_token={}'.format(
    API_HOST, SECRET_TOKEN)


# You might want to get more extensive sample data from here:
# https://raw.githubusercontent.com/OpenBankProject/OBP-API/develop/src/main/scala/code/api/sandbox/example_data/example_import.json


def generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Generates a random string"""
    return ''.join(random.choice(chars) for _ in range(size))


BANK_ID = 'Bank {}'.format(generator())
USER_EMAIL = '{}@foobar.com'.format(generator())
DATA = {
    'banks': [{
        'id': BANK_ID,
        'short_name': 'Bank New',
        'full_name': 'The Bank of New',
        'logo': 'https://static.openbankproject.com/images/sandbox/bank_x.png',
        'website': 'https://www.example.com',
    }],
    'users': [{
        'email': USER_EMAIL,
        'password': 'qwertyuiop',
        'display_name': 'Foo Bar',
    }],
    'accounts': [{
        'id': 'a65e28a5-9abe-428f-85bb-6c3c38122adb',
        'bank': BANK_ID,
        'label': 'New bank account for {}'.format(USER_EMAIL),
        'number': '007',
        'type': 'CURRENT PLUS',
        'balance': {
            'currency': 'GBP',
            'amount': '42',
        },
        'IBAN': 'BA12 1234 5123 4518 4490 1189 007',
        'owners': [USER_EMAIL],
        'generate_public_view': True,
        'generate_accountants_view': True,
        'generate_auditors_view': True,
    }],
}


def import_data():
    """Import sandbox data"""
    print('Posting to {}'.format(URL_IMPORT))
    response = requests.post(URL_IMPORT, json=DATA)
    if response.status_code == 201:
        print('The data has been imported successfully.')
    else:
        print('Status code: {}'.format(response.status_code))
        print(response.text)


if __name__ == '__main__':
    import_data()
