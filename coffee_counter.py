#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#
I created this to know how much competition was making off of donations to 
determine if donationware could be a good model for my service.

Use this nicely please :)

## Requirements
Works with standard packages for `python2` and `python3`.

## How to use it

```
# Generic
python coffee_counter.py <user_id_or_url>

# For example on my page:
python coffee_counter.py https://www.buymeacoffee.com/NrHVy1S
>>> {'coffee_custom_price': 3,
 'currency': 'EUR',
 'currency_sign': '€',
 'num_coffees': 23,
 'num_donors': 10,
 'total_money': 69,
 'username': 'NrHVy1S'}
```
"""

import pprint
import re
import requests

class CouldNotConnect(Exception):
    pass

class CouldNotFindCoffee(Exception):
    pass

class MissingField(Exception):
    pass

def extract_username(username_or_url):
    return username_or_url.rsplit('/')[-1].split('?')[0]    

def get_the_info(username_or_url):
    ''' Fetch the data from Buy Me a Coffee (buymeacoffee.com) and sum up the
    donations for a given creator.'''

    # Get username
    username = extract_username(username_or_url)

    # Fetch generic info including amount per donation
    url = 'https://www.buymeacoffee.com/{}'.format(username)
    res = requests.get(url)
    
    info = dict()
    for field in ['currency', 'currency_sign', 'coffee_custom_price']:
        try:
            info[field] = re.findall('<input type="hidden" id="{}" value="(.*)">'.format(field), res.text)[0]
        except IndexError:
            raise MissingField('Could not find field {}'.format(field))
        try:
            info[field] = int(info[field])
        except:
            pass
    try:
        num_supporters = int(re.findall('([0-9]+) supporters<', res.text)[0])
    except:
        MissingField('Number of supporters')
    
    # Fetch Number of coffees
    url_template = 'https://www.buymeacoffee.com/{}?page={}&notification=1'
    num_coffees = 0
    num_donors = 0
    i = 0
    while True:
        print('At page {}/{}'.format(i+1, num_supporters//5 + 1))
        url = url_template.format(username, i)
        res = requests.get(url)
        
        if res.status_code != 200:
            raise CouldNotConnect
        
        if res.text:
            donations = re.findall("bought ([0-9]+|a+) ", res.text)
            num_donors += len(donations)
            num_coffees += sum(int(x.replace('a', '1')) for x in donations)
            if len(donations) == 0:
                raise CouldNotFindCoffee
            i += 1
        else:
            break
            
        
    # The Money the cash the moolah baby
    info['num_coffees'] = num_coffees
    info['num_donors'] = num_donors
    info['total_money'] = num_coffees * info['coffee_custom_price']
    info['username'] = username
    
    return info

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('username_or_url',
                        help='The buymeacoffee.com username or URL')
    try: 
        username_or_url = parser.parse_args().username_or_url
    except:
        username_or_url = 'NrHVy1S'
    
    info = get_the_info(username_or_url)
    
    print('\nResult:')
    pprint.pprint(info)