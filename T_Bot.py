import string
import os
import pandas as pd
from kucoin.client import Market, User, Trade


#################################### Input Parameters #################################### 

TestNet = True
weeklyAmount = 200

tickr = ['BTC-USDT', 'ETH-USDT']

proportion = {
    'BTC-USDT':0.5,
    'ETH-USDT':0.25}

myThreshold = 0.65



######################################### Set up with API details #########################################

# Laptop


# AWS



if TestNet:
    Net = 'Test Net'
    api_key = os.environ.get('TEST_KC_API_KEY')
    api_secret = os.environ.get('TEST_KC_API_SECRET')
    api_passphrase = os.environ.get('TEST_KC_API_PASS')
    marketclient = Market()
    userclient = User(api_key, api_secret, api_passphrase, is_sandbox=True)
    tradeclient = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)
else:
    Net = 'Main Net'
    api_key = os.environ.get('KC_API_KEY')
    api_secret = os.environ.get('KC_API_SECRET')
    api_passphrase = os.environ.get('KC_API_PASS')
    marketclient = Market()
    userclient = User(api_key, api_secret, api_passphrase)
    tradeclient = Trade(api_key, api_secret, api_passphrase)


account_sid = os.environ.get('TWIL_ACCOUNT_SID')
auth_token = os.environ.get('TWIL_AUTH_TOKEN')

path = '/home/ubuntu/ATH/'




######################################### Function to send text message #########################################

def sendtext(txt):


  from twilio.rest import Client
  twilclient = Client(account_sid, auth_token)
  txt = ''.join(txt)
  print(txt)
  
  '''
  numbers_to_message = ['+447969808650']
  for number in numbers_to_message:
      twilclient.messages.create(
          body = mssgs,
          from_ = '+16814994351',
          to = number
      )
  '''

'''
def TextBalances(capital, hodling):

    capital = round(capital, 2)
    hodling = round(hodling, 5)
    
    message = (
        
        )
        
    print(message)
    sendtext(message)
    
'''

######################################### Function to determine Buy / Sell amount #########################################
'''
These functions are called in f_placeOrder
'''

# Define functions that determine the buy and sell amount
def f_buyAmount(t):
  #Buy amount in proportions as defined initially
  amount = weeklyAmount*proportion[t]
  return amount

######################################### Function to place order #########################################
'''
This function is called in the assess conditions function
'''

def f_placeBuyOrder(buyamount, t):
    try:
      order = tradeclient.create_market_order(t, 'buy', funds=str(round(buyamount, 3)))
      print(order)
      global mssgs
      mssgs.append(f'. \nBuy function successfully executed: ${round(buyamount, 2)} of ' + t + ' purchased.')
    except Exception as e:
      print(f'Error placing order: {e}')

######################################### Assess Opportunity Function #########################################

def f_assessOpp(t, currentprice, ath, threshold):

  buy_amount = f_buyAmount(t)
  sell_amount = 10
  
  global mssgs
  ## If statements to determine action
  if (currentprice < ath*threshold) & (myCapital > buy_amount):
      mssgs.append(f'. \nBuy opportunity identified for ' + t)
      
      f_placeBuyOrder(buy_amount, t)
      
  elif (currentprice < ath*threshold) & (myCapital < buy_amount):
      mssgs.append(f'. \nNot enough funds to action on buy opportunity on ' + t)

      
  elif (currentprice > ath) & (myHodlings*currentprice > sell_amount):
      mssgs.append(f". \nNo sell function defined. Cannot act on opportunity to sell " +t)
      
      #If holdings larger than 0
      #If current price larger than ATH or weighted buy price (sum Fiat spent / sum BTC bought)
      #Linear sell function

  elif (currentprice > ath) & (myHodlings*currentprice < sell_amount): 
      mssgs.append(f". \nNo sell function defined. Cannot act on opportunity to sell " + t)
      
     
  elif (currentprice > ath*threshold) & (currentprice < ath):
      mssgs.append(f'. \nPrice in mid-range. No action to be taken on ' + t)
     

######################################### Pull necessary inputs to functions (e.g. price, holdings, etc) #########################################
'''
These varriables are the input to the 'run' function
'''

mssgs =[]

for t in tickr:

    # Load account and price info
    account = userclient.get_account_list()
    account = pd.DataFrame(account)
    myCapital = float(account[(account['currency'] == 'USDT') & (account['type'] == 'trade')]['balance'].iloc[0])
    myHodlings = float(account[(account['currency'] == t[0:-5]) & (account['type'] == 'trade')]['balance'].iloc[0])
    theCurrentPrice = float(marketclient.get_ticker(symbol=t)['price'])
    
    
    # Read and update API
    file1 = open(path+t[0:-5]+"_ATH.txt", "r")
    theATH = float(file1.read())
    file1.close()
    
    if theCurrentPrice > theATH:
        theATH = theCurrentPrice
        file2 = open(path+t[0:-5]+"_ATH.txt", "w")
        file2.write(str(theCurrentPrice))
        file2.close()
    
     
    f_assessOpp(t, theCurrentPrice, theATH, myThreshold)


sendtext(mssgs)

######################################### Load Account info after execution #########################################


## Load Account info
account = userclient.get_account_list()
account = pd.DataFrame(account)
myCapital = float(account[(account['currency'] == 'USDT') & (account['type'] == 'trade')]['balance'].iloc[0])

mssg = f'. \nRemaining Balance: \nUSDT: ${myCapital}'

if myCapital < weeklyAmount:
    mssg = mssg + f'\nTop Up!'

sendtext(mssg)







