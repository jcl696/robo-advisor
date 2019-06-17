

# app/robo_advisor.py

# Essentially what we want at the end, below

import requests
import json 

requests_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(requests_url)
 

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

#breakpoint()

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) # TODO - SORT: assumes latest day is first to make sure the latest day is first

latest_day = dates[0]

#print(tsd)

latest_day = "2019-02-20"

latest_close = tsd[latest_day]["4. close"]


#breakpoint()


#maximum of the last 100 high prices
#high_price = [10,20,30,40,1233]
#recent_high = max(high_price)


high_prices = []


for date in dates: 
    high_price = tsd[date]["2. high"] 
    high_prices.append(float(high_price))

recent_high = max(high_prices)

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
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


