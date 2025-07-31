#!/usr/bin/env python3
# coding=utf-8

import json
from requests import Session
import os


API_TICKER_URL = 'https://fapi.binance.com/fapi/v2/ticker/price'
API_KLINES_URL = 'https://fapi.binance.com/fapi/v1/klines'
WATCHLIST_FILE = '/home/mirbek/.config/i3blocks/watchlist.json'
numbered_coin = os.environ.get('BLOCK_INSTANCE', 'COIN1')

with open(WATCHLIST_FILE) as f:
    watchlist = json.load(f)

coin = watchlist[numbered_coin]['coin'].upper()

if not coin:
    print('')
    exit(0)

high_stop = watchlist[numbered_coin]['high_stop'] or float('inf')
low_stop = watchlist[numbered_coin]['low_stop']

parameters = {
    'symbol': coin + 'USDT'     # по умолчанию пары берем к USDT
}
# headers = {
#     'Accepts': 'application/json',
#     'X-CMC_PRO_API_KEY': API_KEY,
# }

session = Session()
# session.headers.update(headers)

r = session.get(API_TICKER_URL, params=parameters)
data = json.loads(r.text)
price = float(data['price'])

if price > 100: precision = 0
elif price > 0.1: precision = 5
else: precision = 6

output = ('{}:{:.' + str(precision) + 'f}').format(coin, price)
# output = ('{}:{:.f}').format(coin, price)

if True:
    if price < low_stop:
        output += 'SL'
        print(output) # Short Text
        exit(33)
    elif price > high_stop:
        output += 'TP'
        print(output) # Short Text
        exit(33)

print(output) # Short Text
print("")

# делаем окраску на основе текущей 1H свечи
parameters['interval'] = '1h'
parameters['limit'] = '1'
r = session.get(API_KLINES_URL, params=parameters)
data = json.loads(r.text)
open_price = data[0][1]
close_price = data[0][4]
if open_price > close_price:
    print("#800000")  #soft red
else:
    print("#008000")  #soft green
