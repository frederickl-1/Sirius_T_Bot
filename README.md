# Sirius_T_Bot
Sirius Trading Bot V2 - BTC Only

### TestNet ###

In this version, the following:
- Designed to run once per week and assess buy opportunity at the point of running
- Multi-Currency, proportion dictionary with for loop on chosen tickrs
- Text message sent when purchase is made
- Text message to give account balances (requires further dev)
- API details as environment variables**
- Track ATH in real time
- Threshold set to 0.65

Developments
- Create more if statements in assessment function w. text message
- starting to develop weighted price code

To Do
- Run daily in case when near threshold to buy during daily fluctuations below threshold
- Sell Function
- Improve error handling
-   Error handling run out of Twillio funds
- Limit IP address access of API
- Script to alert when one of the coins we hold are pumping

Other Thoughts
- Can we be more refined? i.e. During a bear market, buy approx weekly but wait for a large drop. Could also look at buying during a bull market when there are large dips
- Intraday trading that capitalises on fluctuations.
