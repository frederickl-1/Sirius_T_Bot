import string
import os
import pandas as pd
from twilio.rest import Client



######################################### Set up with API detaoils #########################################

# Sirius KuCoin Test Net

'''
api_key = os.environ.get('KC_API_KEY') #api_key = "6215534b29c69200011e0027"
api_secret = "8b25ab7f-2a50-44de-8ffc-f0a430040aca"
api_passphrase = "6NAcxQ#gob!$!FUAf4j6#JcooX%&f"

'''
api_key = os.environ.get('KC_API_KEY')
api_secret = os.environ.get('KC_API_SECRET')
api_passphrase = os.environ.get('KC_API_PASS')


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
  auth_token = '498ee4715983e6cde24cc7ae9baa4a75'

  '''
  account_sid = os.environ.get('TWIL_ACCOUNT_SID')
  auth_token = os.environ.get('TWIL_AUTH_TOKEN')
  '''

  client = Client(account_sid, auth_token)

  numbers_to_message = ['+447969808650']#, '+447947964223']
  for number in numbers_to_message:
      client.messages.create(
          body = message,
          from_ = '+19035225966',
          to = number
      )

def TextBalances():

  from kucoin.client import User
  client = User(api_key, api_secret, api_passphrase, is_sandbox=True)
  account = client.get_account_list()
  account = pd.DataFrame(account)

  a = account[['currency', 'balance']]

  Holdings = a.iloc[:,0].to_list()
  Balances = a.iloc[:,1].to_list()

  message = (
      f'Account Balances:'\
      f' {Balances[0]} {Holdings[0]}.'\
      f' {Balances[1]} {Holdings[1]}.'\
      f' {Balances[2]} {Holdings[2]}.'
  )

  print(message)
  sendtext(message)

######################################### Function to determine Buy / Sell amount #########################################
'''
These functions are called in f_placeOrder
'''

# Define functions that determine the buy and sell amount
def f_buyAmount():
  '''
  Currently fixed buy amount, independent of other variables
  '''

  amount = 100

  return amount

def f_sellAmount():
  '''
  Currently fixed sell amount, independent of other variables
  '''

  amount = 100

  return amount


######################################### Function to place order #########################################
'''
This function is called in the assess conditions function
'''

def f_placeBuyOrder(buyamount):

    

    try:

      from kucoin.client import Trade
      client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)
      print(str(round(buyamount/3, 3)))
      order1 = client.create_market_order('ETH-USDT', 'buy', funds=str(round(buyamount/3, 3)))
      print(order1)
      order2 = client.create_market_order('ADA-USDT', 'buy', funds=str(round(buyamount/3, 3)))
      print(order2)
      #order3 = client.create_market_order('MATIC-USDT', 'buy', funds=str(round(buyamount/3, 3)))
      #print(order3)

      from kucoin.client import Market
      client = Market()
      ETHCurrentPrice = float(client.get_ticker(symbol="ETH-USDT")['price'])
      ADACurrentPrice = float(client.get_ticker(symbol="ADA-USDT")['price'])
      MATICCurrentPrice = float(client.get_ticker(symbol="MATIC-USDT")['price'])


      message = (
          f'Buy function successfully executed.'\
          f' ${round(buyamount/3, 2)} of ETH purchased.'\
          f' ${round(buyamount/3, 2)} of ADA purchased.'\
          f' ${round(buyamount/3, 2)} of MATIC purchased.'
      )
      
      print(message)
      sendtext(message)

    except Exception as e:
      print(f'Error placing order: {e}')

#def f_placeSellOrder(sellamount, currentprice):
      



######################################### Assess Opportunity Function #########################################

def f_assessOpp(threshold, ath, currentprice):
  
  if currentprice < ath*threshold: #Buy condition

    buyamount = f_buyAmount()
    f_placeBuyOrder(buyamount)


  if currentprice > ath: #Sell condition

    sellamount = f_sellAmount()
    f_placeSellOrder(sellamount)
      


######################################### Call Function #########################################


def run(myThreshold, theATH, theCurrentPrice):

  f_assessOpp(myThreshold, theATH, theCurrentPrice)

  TextBalances()
    
 
run(myThreshold, theATH, theCurrentPrice)

