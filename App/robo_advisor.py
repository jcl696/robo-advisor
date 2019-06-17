

# app/robo_advisor.py

# Essentially what we want at the end, below

import requests
import json 

requests_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(requests_url)
 

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

# > $1,000
latest_close = parsed_response["Time Series (Daily)"]["2019-02-20"]["4. close"]


#breakpoint()


def to_usd(my_price): #reference an int or flaot with to_usd to get the dollar sign and correct decimals
    return "${0:,.2f}".format(my_price)







print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm") #TODO - use the datetime module to do this
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


