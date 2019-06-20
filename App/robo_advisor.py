

# app/robo_advisor.py

# Essentially what we want at the end, below

#KEEP MODULES BEFORE PACKAGES

#TODO - BRING IN THE CSV MODULE AND START WRITING 
import datetime
import csv
import json
import os
from dotenv import load_dotenv

import requests

load_dotenv()

#TODO - Make stock choice an input with a fail message if the stock is wrong
# use the datetime module to do this  ----> DONE
# recommendaiton and reason 

#stock_choice = input("What stock would you like to have analyzed today? ")


# Checking for errors in the input 
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")


while True:
    stock_choice = input("What stock would you like to have analyzed today? ")
    requests_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_choice}&apikey={API_KEY}"
    response = requests.get(requests_url)
    if "Error" in response.text:
        print("The stock you submitted doesn't exist.")
        #print(response.text)
    
    else: 
        break 


parsed_response = json.loads(response.text)
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

#formatted_last_refreshed = datetime.datetime.strptime(last_refreshed, "%Y-%m-%d %H:%M:%S")


#breakpoint()

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) # TODO - SORT: assumes latest day is first to make sure the latest day is first

#dates.sort()

sorted_dates = sorted(dates, reverse=True) #reverse=True in sorted function gives you control over sorting


latest_day = sorted_dates[0]  # > 2019-06-17


#print(tsd)

latest_close = tsd[latest_day]["4. close"]


#breakpoint()


#maximum of the last 100 high prices
#high_price = [10,20,30,40,1233]
#recent_high = max(high_price)


high_prices = []
low_prices = []
close_prices = []
volumes = []

for date in dates: 
    high_price = tsd[date]["2. high"] 
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))
    close_price = tsd[date]["4. close"]
    close_prices.append(float(close_price))
    volume = tsd[date]["5. volume"]
    volumes.append(int(volume))

recent_high = max(high_prices)
recent_low = min(low_prices)
avg_volume = int(sum(volumes) / len(volumes))
avg_close = sum(close_prices) / len(close_prices)
latest_volume = int(tsd[latest_day]["5. volume"])


def to_usd(my_price): #reference an int or flaot with to_usd' to get the dollar sign and correct decimals
    return "${0:,.2f}".format(my_price)


csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
#csv_file_path = "app/prices.csv" # a relative filepath

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]


with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames= csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        
        writer.writerow({"timestamp": date, 
        "open": daily_prices["1. open"], 
        "high": daily_prices["2. high"], 
        "low": daily_prices["3. low"], 
        "close": daily_prices["4. close"], 
        "volume": daily_prices["5. volume"]})
    
    
    #
    #writer.writerow({"city": "New York", "name": "Mets"})
    #writer.writerow({"city": "Boston", "name": "Red Sox"})
    #writer.writerow({"city": "New Haven", "name": "Ravens"})
#

now = datetime.datetime.now()
right_now = (now.strftime("%Y-%m-%d %H:%M:%S %p"))


print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {right_now}")  
print("-------------------------")
print(f"MARKET DATA LAST REFRESHED: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")

if avg_volume > (latest_volume):
    print("RECOMMENDATION: BUY!") 
    print("RECOMMENDATION REASON: The latest volume is less than the recent average volume, because of this it will be more likely that you will get to buy the stock at the price you want.")

else:
    print("RECOMMENDATION: SELL!")
    print("RECOMMENDATION REASON: Since there is more volume in the market, there is more liquidity and you can sell your stock easier, hopefully for a gain!")




print("-------------------------")
print(f"WRITE DATA TO CSV: {csv_file_path}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


 
