import string
import os
import pandas as pd


######################################### Set up with API details #########################################

# Sirius KuCoin Test Net


api_key = "621a1b182b968a0001530eac"
api_secret = "1c4aad2c-899c-4be7-b188-48901251b7cd"
api_passphrase = "6215534b29c69200011e0027"

account_sid = 'ACe4dae2d7377a52438c4d4b6d8d53ed60'
auth_token = 'b9e08169dba1485c8121184fd89356ff'



'''

api_key = os.environ.get('KC_API_KEY')
api_secret = os.environ.get('KC_API_SECRET')
api_passphrase = os.environ.get('KC_API_PASS')

account_sid = os.environ.get('TWIL_ACCOUNT_SID')
auth_token = os.environ.get('TWIL_AUTH_TOKEN')
'''

######################################### Pull necessary inputs to functions (e.g. price, holdings, etc) #########################################
'''
These varriables are the input to the 'run' function
'''


from kucoin.client import User
userclient = User(api_key, api_secret, api_passphrase, is_sandbox=True)

from kucoin.client import Market
marketclient = Market()

from kucoin.client import Trade
tradeclient = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)

from twilio.rest import Client
twilclient = Client(account_sid, auth_token)
      
# Load in ATH from text file
file1 = open("ATH_tracker.txt", "r")
theATH = float(file1.read())
file1.close()


# Load Current Price from Market


theCurrentPrice = float(marketclient.get_ticker(symbol="BTC-USDT")['price'])


if theCurrentPrice > theATH:
    file2 = open("ATH_tracker.txt", "w")
    file2.write(str(theCurrentPrice))
    file2.close()
    



## Set other required variables
myThreshold = 0.65



print(f'PiggyBank contains ${myCapital} USDT')
print(f'PiggyBank contains {myHodlings} BTC')
print(f'Current price of BTC is ${theCurrentPrice}')

######################################### Function to send text message #########################################

def sendtext(message):

  numbers_to_message = ['+447969808650']
  for number in numbers_to_message:
      twilclient.messages.create(
          body = message,
          from_ = '+16814994351',
          to = number
      )
      
      
def TextBalances(capital, hodling):


    '''
    from kucoin.client import User
    client = User(api_key, api_secret, api_passphrase, is_sandbox=True)
    account = client.get_account_list()
    account = pd.DataFrame(account)
      
    a = account[['currency', 'balance']]
      
    Holdings = a.iloc[:,0].to_list()
    Balances = a.iloc[:,1].to_list()
          
    '''
    capital = round(capital, 2)
    hodling = round(hodling, 2)
    
    message = (
        f'Account Balances:'
        f' USDT: ${capital} /'
        f' BTC: {hodling}'
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


def f_sellAmount(dollar_value_hodling):
  '''
  Sell 5% of hodlings
  '''
  
  amount = dollar_value_hodling
  amount = 0.05*amount
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
          f'Buy function successfully executed.'\
          f' ${round(buyamount, 2)} of BTC purchased.'
      )
      print(message)
      #sendtext(message)
    except Exception as e:
      print(f'Error placing order: {e}')


def f_placeSellOrder(sellamount):
    try:
      order = tradeclient.create_market_order('BTC-USDT', 'sell', funds=str(round(sellamount, 3)))
      print(order)
      message = (
          f'Sell function successfully executed.'\
          f' ${round(sellamount, 2)} of BTC sold.'
      )
      print(message)
      #sendtext(message)
    except Exception as e:
      print(f'Error placing order: {e}')


######################################### Assess Opportunity Function #########################################

def f_assessOpp():

  currentprice = theCurrentPrice
  ath = theATH
  threshold = myThreshold
  
  ## My Holdings
  account = userclient.get_account_list()
  account = pd.DataFrame(account)
  myCapital = float(account[account['currency'] == 'USDT']['balance'].iloc[0])
  myHodlings = float(account[account['currency'] == 'BTC']['balance'].iloc[0])
  
  ## Weighted price  
  orders = tradeclient.get_order_list(symbol="BTC-USDT", status='done', side='buy')

  
  ## If statements to determine action
  if (currentprice < ath*threshold) & (myCapital > 100):
      
      message = f'Buy opportunity identified'
      print(message)
      #sendtext(message)
      
      buyamount = f_buyAmount()
      f_placeBuyOrder(buyamount)
      
  elif (currentprice < ath*threshold) & (myCapital < 100):
      
      message = f'Not enough funds to action on buy opportunity'
      print(message)
      #sendtext(message)
      
      

  elif (currentprice > ath) & (myHodlings*currentprice > 100):
      message = f'Sell opportunity identified'
      print(message)
      #sendtext(message)
      
      sellamount = f_sellAmount(myHodlings*currentprice)
      f_placeSellOrder(sellamount)
      #If holdings larger than 0
      #If current price larger than ATH or weighted buy price (sum Fiat spent / sum BTC bought)
      #Linear sell function

  elif (currentprice > ath) & (myHodlings*currentprice < 100):
        
     message = f'Run out of BTC. Cant action sell opportunity'
     print(message)
     #sendtext(message)
      
     
     
  elif (currentprice > ath*threshold) & (currentprice < ath):
     message = f'Price in mid-range. No action to be taken'
     print(message)
     #sendtext(message)      

    
  TextBalances(myCapital, myHodlings)



######################################### Call Function #########################################



f_assessOpp()




## Weighted price  
orders = tradeclient.get_order_list(symbol="BTC-USDT", status='done', side='buy')

orders = orders['items']
orders = pd.DataFrame(orders)
orders[['size', 'funds']] = orders[['size','funds']].astype(float)
boughtamount = orders[orders['side']=='buy']['size'].sum(0)
