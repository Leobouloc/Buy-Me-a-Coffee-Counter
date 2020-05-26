# Buy-Me-a-Coffee-Counter
Count the number of coffees bought on buymeacoffee.com

I made this to know how much competition was making off of donations to 
determine if donationware could be a good model for my service. Use this nicely please :)

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
