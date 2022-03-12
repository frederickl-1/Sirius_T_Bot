import string
import os
import pandas as pd


######################################### Set up with API details #########################################

# Sirius KuCoin Test Net

api_key = os.environ.get('KC_API_KEY')
api_secret = os.environ.get('KC_API_SECRET')
api_passphrase = os.environ.get('KC_API_PASS')

account_sid = os.environ.get('TWIL_ACCOUNT_SID')
auth_token = os.environ.get('TWIL_AUTH_TOKEN')


######################################### Pull necessary inputs to functions (e.g. price, holdings, etc) #########################################
'''
These varriables are the input to the 'run' function
'''


from kucoin.client import User
userclient = User(api_key, api_secret, api_passphrase)#, is_sandbox=True)

from kucoin.client import Market
marketclient = Market()

from kucoin.client import Trade
tradeclient = Trade(api_key, api_secret, api_passphrase)#, is_sandbox=True)

## Load Account info
account = userclient.get_account_list()
account = pd.DataFrame(account)
myCapital = float(account[(account['currency'] == 'USDT') & (account['type'] == 'trade')]['balance'].iloc[0])
myHodlings = float(account[(account['currency'] == 'BTC') & (account['type'] == 'trade')]['balance'].iloc[0])


# Load Current Price from Market
theCurrentPrice = float(marketclient.get_ticker(symbol="BTC-USDT")['price'])


# Load and update ATH
file1 = open("/home/ubuntu/Sirius_T_Bot/ATH_tracker.txt", "r")
#file1 = open("ATH_tracker.txt", "r")
theATH = float(file1.read())
file1.close()

if theCurrentPrice > theATH:
    file2 = open("/home/ubuntu/Sirius_T_Bot/ATH_tracker.txt", "w")
    #file2 = open("ATH_tracker.txt", "w")
    file2.write(str(theCurrentPrice))
    file2.close()
    


## Set other required variables
myThreshold = 0.65




######################################### Function to send text message #########################################

def sendtext(message):


  from twilio.rest import Client
  twilclient = Client(account_sid, auth_token)
  
  numbers_to_message = ['+447969808650']
  for number in numbers_to_message:
      twilclient.messages.create(
          body = message,
          from_ = '+16814994351',
          to = number
      )
      
      
def TextBalances(capital, hodling):

    capital = round(capital, 2)
    hodling = round(hodling, 5)
    
    message = (
        f'. \nAccount Balances: \nUSDT: ${capital} \nBTC: {hodling}'
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

  amount = 5
  return amount


######################################### Function to place order #########################################
'''
This function is called in the assess conditions function
'''

def f_placeBuyOrder(buyamount):
    try:
      order = tradeclient.create_market_order('BTC-USDT', 'buy', funds=str(round(buyamount, 3)))
      print(order)
      message = (
          f'. \nBuy function successfully executed: \n${round(buyamount, 2)} of BTC purchased.'
      )
      print(message)
      sendtext(message)
    except Exception as e:
      print(f'Error placing order: {e}')

######################################### Assess Opportunity Function #########################################

def f_assessOpp():

  currentprice = theCurrentPrice
  ath = theATH
  threshold = myThreshold
  
  
  ## Weighted price  
  orders = tradeclient.get_order_list(symbol="BTC-USDT", status='done', side='buy')

  
  ## If statements to determine action
  if (currentprice < ath*threshold) & (myCapital > 10):
      
      message = f'. \nBuy opportunity identified'
      print(message)
      sendtext(message)
      
      buyamount = f_buyAmount()
      f_placeBuyOrder(buyamount)
      
  elif (currentprice < ath*threshold) & (myCapital < 10):
      
      message = f'. \nNot enough funds to action on buy opportunity'
      print(message)
      sendtext(message)
      
      

  elif (currentprice > ath) & (myHodlings*currentprice > 10):
      message = f". \nNo sell function defined. Cannot act on opportunity"
      print(message)
      sendtext(message)
      
      sellamount = f_sellAmount(myHodlings*currentprice)
      f_placeSellOrder(sellamount)
      #If holdings larger than 0
      #If current price larger than ATH or weighted buy price (sum Fiat spent / sum BTC bought)
      #Linear sell function

  elif (currentprice > ath) & (myHodlings*currentprice < 10):
        
     message = f". \nNo sell function defined. Cannot act on opportunity"
     print(message)
     sendtext(message)
      
     
     
  elif (currentprice > ath*threshold) & (currentprice < ath):
     message = f'. \nPrice in mid-range. No action to be taken'
     print(message)
     sendtext(message)      



######################################### Call Function #########################################

f_assessOpp()

######################################### Load Account info after execution #########################################

## Load Account info
account = userclient.get_account_list()
account = pd.DataFrame(account)
myCapital = float(account[(account['currency'] == 'USDT') & (account['type'] == 'trade')]['balance'].iloc[0])
myHodlings = float(account[(account['currency'] == 'BTC') & (account['type'] == 'trade')]['balance'].iloc[0])

TextBalances(myCapital, myHodlings)


  
