import pybithumb
import time
import pandas as pd
import datetime


con_key = "81fc1e8cc7084dbf612699205fbe6070"
sec_key = "cbfd5b509236a62cb870a537a6ca3342"
bithumb = pybithumb.Bithumb(con_key, sec_key)


def get_target_price(ticker):
    df=pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    yesterday_close = yesterday['close']
    ratio = 0.5
    target = ((yesterday_high-yesterday_low)*ratio)+yesterday_close
    return(target)

def buy_crypto(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker,"/KRW")
    sell_price = orderbook['asks'][0]['price']
    unit = krw / float(sell_price * 1.02)
    bithumb.buy_market_order(ticker, unit)


now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

while True:
     now = datetime.datetime.now()
     if mid < now < mid + datetime.delta(seconds=10) :
         print("정각입니다")
         mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

     time.sleep(1)

    tickers = pybithumb.get_tickers()
    print(datetime.datetime.now())
    for ticker in tickers:
        target = get_target_price(ticker)
        current_price = pybithumb.get_current_price(ticker)
        krw = bithumb.get_balance(ticker)[2]
        print(ticker)
        if current_price>=target:
            orderbook = pybithumb.get_orderbook(ticker+"/KRW")
            sell_price = orderbook['asks'][0]['price']
            unit = krw / float(sell_price * 1.02)
            bithumb.buy_market_order(ticker, unit)
            print(ticker+"bought")
    time.sleep(1)


