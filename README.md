# Sirius_T_Bot
Sirius Trading Bot V2

### TestNet ###

In this version, the following:
- KuCoin API using Sandbox account
- Designed to run once per week and assess buy opportunity at the point of running
- **Multiple Currency Pair (ETH, ADA MATIC) - Currently MATIC commented out due to testnet**
- **Fixed weekly purchase amount is apportioned amongst currencies if BTC below certain threshold**
- Text message sent when purchase is made
- **Text message to give account balances (requires further dev)**
- **Updated the install python libraries script**

- **Threshold set to 0.9**


Current Bugs:
- Need to update API variables in script
- Code not letting me place multiple orders at the same time


To Do
- Track ATH in real time
-   Funtion to read and write from a text file
-   Creates text file if none exists
- Improve error handling
-   Error handling run out of Twillio funds
-  **Make API details into environment variables**
- Limit IP address access of API
- Sell function that acts based on the price of currencies held
- Script to alert when one of the coins we hold are pumping

Other Thoughts
- Can we be more refined? i.e. During a bear market, buy approx weekly but wait for a large drop. Could also look at buying during a bull market when there are large dips
- Intraday trading that capitalises on fluctuations.
