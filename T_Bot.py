import json
import requests
import string
import os
from twilio.rest import Client



######################################### Set up with API detaoils #########################################

# Sirius KuCoin Test Net
api_key = "6215534b29c69200011e0027"
api_secret = "8b25ab7f-2a50-44de-8ffc-f0a430040aca"
api_passphrase = "6NAcxQ#gob!$!FUAf4j6#JcooX%&f"



######################################### Pull necessary inputs to functions (e.g. price, holdings, etc) #########################################
'''
These varriables are the input to the run function
'''

## Current Price
from kucoin.client import Market
client = Market()
theCurrentPrice = float(client.get_ticker(symbol="BTC-USDT")['price'])


## My Holdings
from kucoin.client import User
client = User(api_key, api_secret, api_passphrase, is_sandbox=True)
account = client.get_account_list()
account = pd.DataFrame(account)
myCapital = float(account[account['currency'] == 'USDT']['balance'].iloc[0])
myHodlings = float(account[account['currency'] == 'BTC']['balance'].iloc[0])


## Set other required variables
myThreshold = 0.9
theATH = 69044.77


print(f'PiggyBank contains ${myCapital} USDT')
print(f'PiggyBank contains {myHodlings} BTC')
print(f'Current price of BTC is ${theCurrentPrice}')

######################################### Function to send text message #########################################

def sendtext(message):

  import os
  from twilio.rest import Client

  account_sid = 'ACfa019028d2069cd11fc93988692a8b0d'
  auth_token = 'b84fb2af62e0167d0af4e39e8a3ff776'

  client = Client(account_sid, auth_token)

  numbers_to_message = ['+447969808650']#, '+447947964223']
  for number in numbers_to_message:
      client.messages.create(
          body = message,
          from_ = '+19035225966',
          to = number
      )



######################################### Function to determine Buy / Sell amount #########################################
'''
These functions are called in f_placeOrder
'''

# Define functions that determine the buy and sell amount
def f_buyAmount(ath, currentprice):
  '''
  Currently fixed buy amount, independent of other variables
  '''

  x1 = 0.7*ath
  y1 = 100
  x2 = 0.5*ath
  y2 = 500
    
  a = (y2 - y1)/(x2 - x1)
  b = y1 - a*x1
  y = a*currentprice + b

  amount = round(y, 4)

  return amount

def f_sellAmount(ath, currentprice):
  '''
  Currently fixed sell amount, independent of other variables
  '''

  x1 = 1*ath
  y1 = 100
  x2 = 1.5*ath
  y2 = 500
    
  a = (y2 - y1)/(x2 - x1)
  b = y1 - a*x1
  y = a*currentprice + b

  amount = round(y, 4)

  return amount


######################################### Function to place order #########################################
'''
This function is called in the assess conditions function
'''

def f_placeBuyOrder(buyamount, currentprice):

    from kucoin.client import Trade
    client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)

    try:
      print(str(buyamount))
      order = client.create_market_order('BTC-USDT', 'buy', funds=str(buyamount))
      message = f'Durka Durka. Buy function successfully executed. {round(buyamount/currentprice,4)} BTC purchased for ${round(buyamount, 2)}. Mert is a baghead'
      print(order)
      print(message)
      sendtext(message)
    except Exception as e:
      print(f'Error placing order: {e}')

#def f_placeSellOrder(sellamount, currentprice):
      



######################################### Assess Opportunity Function #########################################

def f_assessOpp(threshold, ath, currentprice):
  
  if currentprice < ath*threshold: #Buy condition

    buyamount = f_buyAmount(ath, currentprice)
    f_placeBuyOrder(buyamount, currentprice)


  if currentprice > ath: #Sell condition

    sellamount = f_sellAmount(ath, currentprice)
    f_placeSellOrder(sellamount, currentprice)
      


######################################### Call Function #########################################


def run(myThreshold, theATH, theCurrentPrice):

  f_assessOpp(myThreshold, theATH, theCurrentPrice)

    
 
run(myThreshold, theATH, theCurrentPrice)
