

import json
import requests
import pandas as pd
import time
import hmac
import base64
import hashlib
import secrets
import string
import matplotlib.pyplot as plt
from datetime import datetime



######################################### Set up with API detaoils #########################################
'''
These varriables are the input to the run function
'''


api_key = 'AoQYMcopeJ5g7rv7vUZNcRbdENh0r3rnF4oJNTEu1wCEz82qYVcTfcYOw4XmGQ2Q'
api_secret = 'JhYc61rBihBAJZldpYQDxwcGZpgp5h3xj5OX1m8uWSjQDMkProgpLg0fd0aRUgkD'

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

client = Client(api_key, api_secret) #Store key and secret
client.API_URL = 'https://testnet.binance.vision/api' #Manually change url so we can use test environment

#api_key = "fzDbyqd7z1hZyMmFAc9yfjoHIxG5nWUou0h17l22067Wi7CXtStku3CVX5GFkaHS"
#api_secret = "2uoiC4c2XPygdd1zApuJgTQAHAcVGxva7cMdEvyYJFr4tdnWieKQqLBLcSY94NP3"



######################################### Pull current price and available balance #########################################
'''
These varriables are the input to the run function
'''

myCapital = float(client.get_asset_balance(asset='USDT')['free'])
myHodlings = float(client.get_asset_balance(asset='BTC')['free'])
theCurrentPrice = float(client.get_symbol_ticker(symbol="BTCUSDT")['price'])
myThreshold = 0.9
theATH = 69044.77

print(f'PiggyBank contains ${myCapital} USDT')
print(f'PiggyBank contains {myHodlings} BTC')
print(f'Current price of BTC is ${currentPrice}')


######################################### Function to determine Buy / Sell amount #########################################
'''
These functions are called in f_placeOrder
'''

# Define functions that determine the buy and sell amount
def f_buyAmount():
  '''
  Currently fixed buy amount, independent of other variables
  '''
  amount = 200
  return amount

def f_sellAmount():
  '''
  Currently fixed sell amount, independent of other variables
  '''
  amount = 200
  return amount


######################################### Function to place order #########################################
'''
This function is called in the assess conditions function
'''

def f_placeBuyOrder(buyamount, currentprice):

    try:
      order = client.order_market_buy(
          symbol='BTCUSDT',
          quantity=round(buyamount/currentprice, 4))
      print(f'{quantity} BTC purchased for ${buyamount})
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        print(e)

def f_placeSellOrder(buyamount, currentprice):
      
    try:
      order = client.order_market_sell(
          symbol='BTCUSDT',
          quantity=round(buyamount/currentprice, 4))
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        print(e)



######################################### Assess Opportunity Function #########################################

def f_assessOpp(threshold, ath, currentprice):
  
  if currentPrice < ath*threshold: #Buy condition

    buyamount = f_buyAmount()
    f_placeBuyOrder(buyamount, currentprice)


  if currentPrice > ath: #Sell condition

    sellamount = f_sellAmount()
    f_placeSellOrder(sellamount, currentprice)
      


######################################### Call Function #########################################


def run(myThreshold, theATH, theCurrentPrice):

  f_assessOpp(myThreshold, theATH, theCurrentPrice):

    
 

run(myThreshold, theATH, theCurrentPrice)
