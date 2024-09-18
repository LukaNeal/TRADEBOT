from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus, TimeInForce
from alpaca.data.live import StockDataStream
from alpaca.data import StockHistoricalDataClient, StockTradesRequest
from datetime import datetime, timedelta, time
from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
import alpaca_trade_api as tradeapi
import requests
import json
import os


#ALPACA API KEYS
BASE_URL = 
KEY_ID = 
SECRET_KEY = 

#Specifying accounts for data and trading
history_account = StockHistoricalDataClient(KEY_ID, SECRET_KEY)
account = TradingClient(KEY_ID, SECRET_KEY, paper=True)

#asking which stock you want to run the algo on
stock_symbol = str(input("What do you want to trade?")).strip()

trade_data = StockTradesRequest(
    symbol_or_symbols = stock_symbol,
    timeframe = TimeFrame.Day,
    start = datetime.now()-timedelta(minutes = 1),
    end = datetime.now(),
    limit = 100
)
past_minute_trades = (str(history_account.get_stock_trades(trade_data)))

#data sets for limit buys and normal buys
order_data = MarketOrderRequest(
    symbol = stock_symbol,
    qty = 1,
    side = OrderSide.BUY,
    time_in_force = TimeInForce.DAY
   )

limit_order_data = LimitOrderRequest(
    symbol = stock_symbol,
    qty = 1,
    side = OrderSide.BUY,
    time_in_force = TimeInForce.DAY,
    limit_price = 300.00 #this is just a random number
   )

sell_data = MarketOrderRequest(
    symbol = stock_symbol,
    qty = 1,
    side = OrderSide.SELL,
    time_in_force = TimeInForce.DAY
)

# buy function for placing market orders
def buy():
    order = account.submit_order(order_data)
    print(order)

# buy function for placing limit orders
def limitbuy():
    limitorder = account.submit_order(limit_order_data)

#sell function

def sell():
    order = account.submit_order(sell_data)
    print(order)

openai_api_key = "put your key here"

if openai_api_key is None:
    raise ValueError("OpenAI API key is not set in environment variables.")

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}

data = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": f"Should I buy or sell {stock_symbol} based on the trades presented here: {past_minute_trades}? please analyze the market data and give a definitive one-word answer that's either Buy. or Sell."
        }
    ]
}

response = requests.post(url, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    print("Response from OpenAI:", response.json())
    print('\n')
    print(response.json()['choices'][0]['message']['content'])
else:
    print("Error:", response.status_code, response.text)

#Automate the trades based on the response from the API
if (response.json()['choices'][0]['message']['content']) == "Buy.":
    buy()
elif (response.json()['choices'][0]['message']['content']) == "Sell.":
    sell()
else:
    print("No trade made.")
