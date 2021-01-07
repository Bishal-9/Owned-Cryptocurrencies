import requests
import datetime
from prettytable import PrettyTable
from colorama import Fore, Back, Style

convert = 'INR'

listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert=' + convert

request = requests.get(url=listings_url, headers={'X-CMC_PRO_API_KEY': 'Your_API_Key'})
result = request.json()
data = result['data']

ticker_url_pairs = {}
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    ticker_url_pairs[symbol] = url

print()
print('MY PORTFOLIO')
print()

portfolio_value = 0.00
last_updated = 0

table = PrettyTable(['Asset', 'Amount Owned', convert + ' Value', 'Price', '1h', '24h', '7d'])

with open('portfolio.txt') as inp:
    for line in inp:
        ticker, amount = line.split()
        ticker = ticker.upper()

        ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=' + ticker + '&convert=' + convert

        request = requests.get(url=ticker_url, headers={'X-CMC_PRO_API_KEY': 'Your_API_Key'})
        results = request.json()

        currency = results['data'][ticker]
        name = currency['name']
        last_updated = currency['last_updated']
        symbol = currency['symbol']
        quotes = currency['quote'][convert]
        hour_change = quotes['percent_change_1h']
        day_change = quotes['percent_change_24h']
        week_change = quotes['percent_change_7d']
        price = quotes['price']

        value = float(price) * float(amount)

        if hour_change > 0:
            hour_change = Back.GREEN + Fore.BLACK + str(hour_change) + '%' + Style.RESET_ALL
        else:
            hour_change = Back.RED + Fore.BLACK + str(hour_change) + '%' + Style.RESET_ALL
        if day_change > 0:
            day_change = Back.GREEN + Fore.BLACK + str(day_change) + '%' + Style.RESET_ALL
        else:
            day_change = Back.RED + Fore.BLACK + str(day_change) + '%' + Style.RESET_ALL
        if week_change > 0:
            week_change = Back.GREEN + Fore.BLACK + str(week_change) + '%' + Style.RESET_ALL
        else:
            week_change = Back.RED + Fore.BLACK + str(week_change) + '%' + Style.RESET_ALL

        portfolio_value += value

        value_string = '{:,}'.format(round(value, 2))

        table.add_row([
            name + ' (' + symbol + ')',
            amount,
            '₹' + value_string,
            '₹' + str(price),
            str(hour_change),
            str(day_change),
            str(week_change)
        ])

print(table)
print()

portfolio_value_string = '{:,}'.format(round(portfolio_value, 2))
last_updated_string = datetime.datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ")

print('Total Portfolio Value: ' + Back.GREEN + Fore.BLACK + '₹' + str(portfolio_value_string) + Style.RESET_ALL)
print()
print('API Results Last Updated on ' + str(last_updated_string))
print()