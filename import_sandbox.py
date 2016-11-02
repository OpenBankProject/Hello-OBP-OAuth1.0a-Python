#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Imports sample data into your sandbox
"""

import random
import string

from oauth_dance import get_api
from settings import API_BASE_URL


URL_IMPORT = '{}/sandbox/data-import'.format(API_BASE_URL)


# You might want to get more extensive sample data from here:
# https://raw.githubusercontent.com/OpenBankProject/OBP-API/develop/src/main/scala/code/api/sandbox/example_data/example_import.json


def generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Generates a random string"""
    return ''.join(random.choice(chars) for _ in range(size))


BANK_ID = 'Bank {}'.format(generator())
DATA = {
    'banks': [{
        'id': BANK_ID,
        'short_name': 'Bank New',
        'full_name': 'The Bank of New',
        'logo': 'https://static.openbankproject.com/images/sandbox/bank_x.png',
        'website': 'https://www.example.com',
    }],
}


def import_data():
    """Import sandbox data"""
    api = get_api()
    print('Posting data to {}'.format(URL_IMPORT))
    response = api.post(URL_IMPORT, json=DATA)
    if response.status_code == 201:
        print('The data has been imported successfully.')
    else:
        print('Status code: {}'.format(response.status_code))
        print(response.text)


if __name__ == '__main__':
    import_data()
