from sys import argv

import pandas as pd
import yfinance as yf
import sqlite3

#function that downloads data

def get_stock_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    data.reset_index(inplace=True)
    data.rename(columns={
        "Date": "date",
        "Open": "open",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume"
    }, inplace=True)
    data['symbol'] = symbol
    return data

#function that uses the prior data and saves it into a databse
def save_data_range(symbol, start, end, con):
    data = get_stock_data(symbol, start, end)
    data.to_sql(
        "stock_data", 
        con, 
        if_exists="append", 
        index=False
    )

#function that saves the last trading day's data into the database
def save_last_trading_session(symbol, con):
    today = pd.Timestamp.today()
    data = get_stock_data(symbol, today, today)
    data.to_sql(
        "stock_data", 
        con, 
        if_exists="append", 
        index=False
    )

if __name__ == "__main__":
    # usage example for bulk insert
    #     python market_data.py bulk SPY 2022-01-01 2022-10-20
    # usage example for last session
    #     python market_aata.py last SPY

    con = sqlite3.connect("market_data.sqlite")

    if argv[1] == "bulk":
        symbol = argv[2]
        start = argv[3]
        end = argv[4]
        save_data_range(symbol, start, end, con)
        print(f"{symbol} saved between {start} and {end}")
    elif argv[1] == "last":
        symbol = argv[2]
        save_last_trading_session(symbol, con)
        print(f"{symbol} saved")
    else:
        print("Enter bulk or last")