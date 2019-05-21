import requests

URL = 'https://yobit.net/api/2/'
ticker = '/ticker'


def get_btc():
    url = URL + 'btc_usd' + ticker
    print(url)
    response = requests.get(url).json()

    buying_price = response['ticker']['buy']
    selling_price = response['ticker']['sell']
    
    last = '''Buying price: {} USD
Selling price: {} USD'''.format(buying_price, selling_price)
            
    return last

get_btc()

