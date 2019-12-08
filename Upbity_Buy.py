import pyupbit
import time

con_key = "g84pSKocX46FRjpSdSmxxyGJ8rV7q5KHpCNVOalx"
sec_key = "SpZmxIuIa4w3xmj3BCCM3Foibaa1xn6n8KDoEOiS"
upbit = pyupbit.Upbit(con_key, sec_key)
tickers = pyupbit.get_tickers(fiat="KRW")


def get_target_price(ticker):
    df= pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    yesterday_close = yesterday['close']
    ratio = 0.49
    target = ((yesterday_high-yesterday_low)*ratio)+yesterday_close
    return target

while True:
    for ticker in tickers:
        target = get_target_price(ticker)
        current_price = pyupbit.get_current_price(ticker)
        price_info = pyupbit.get_ohlcv(ticker)
        today_price = price_info.iloc[-1]
        today_high = today_price['high']
        today_open = today_price['open']
        today_max= (today_high-today_open)/today_open
        # yesterday_info= price_info.iloc[-2]
        # yesterday_volume = yesterday_info['volume']*yesterday_info['close']
        if current_price>=target and today_max>0.04: # yesterday volume 100분의 1 에 한해 가능한 밸런스
            krw = 1000
            orderbook = pyupbit.get_orderbook(ticker)
            sell_price = orderbook[0]['orderbook_units'][3]['ask_price']
            unit = krw / sell_price
            print(upbit.buy_limit_order(ticker,sell_price,unit))
            time.sleep(0.5)
            print(upbit.sell_limit_order(ticker, sell_price*1.3,unit))
        time.sleep(0.1)




