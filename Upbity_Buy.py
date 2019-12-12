import pyupbit
import time
import datetime

con_key = "g84pSKocX46FRjpSdSmxxyGJ8rV7q5KHpCNVOalx"
sec_key = "SpZmxIuIa4w3xmj3BCCM3Foibaa1xn6n8KDoEOiS"
upbit = pyupbit.Upbit(con_key, sec_key)
tickers = pyupbit.get_tickers(fiat="KRW")


def get_target_price(tick):
    df= pyupbit.get_ohlcv(tick)
    yesterday = df.iloc[-2]
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    yesterday_close = yesterday['close']
    ratio = 0.49
    target = ((yesterday_high-yesterday_low)*ratio)+yesterday_close
    return target

while True:
    print(datetime.datetime.now())
    hold_balance = upbit.get_balances()[0]
    hold_list = []
    for i in hold_balance:
        hold_list.append("KRW-"+i['currency'])
    buy_target = set(tickers) - set(hold_list) #매수주문이 대기상태인 코인들을 안빼고있음
    for tick in buy_target:
        target = get_target_price(tick)
        current_price = pyupbit.get_current_price(tick)
        price_info = pyupbit.get_ohlcv(tick)
        today_price = price_info.iloc[-1]
        today_high = today_price['high']
        today_open = today_price['open']
        today_max = (today_high-today_open)/today_open
        yes = pyupbit.get_daily_ohlcv_from_base(tick).iloc[-2]
        yes_vol = yes['close']*yes['volume']
        time.sleep(0.1)
        if current_price>=target and today_max<0.1 and yes_vol>150000000:
            # yesterday volume 100분의 1 에 한해 가능한 밸런스를 오더넣는거 구현 필요
            #
            krw = 1000
            orderbook = pyupbit.get_orderbook(tick)
            price = orderbook[0]['orderbook_units'][0]['bid_price']
            unit = format((krw / price),'.2f')
            print(tick)
            print(upbit.buy_limit_order(tick,price,unit))

        hold_balance = upbit.get_balances()[0]
        for i in hold_balance[1:]:
            sell_price = float(i['avg_buy_price']) * 1.28
            if sell_price < 10:
                adj_sell_price = format(sell_price, '.2f')
            elif 10 <= sell_price < 100:
                adj_sell_price = format(sell_price, '.1f')
            elif 100 <= sell_price < 1000:
                adj_sell_price = round(sell_price)
            elif 1000 <= sell_price < 10000:
                adj_sell_price = sell_price - (sell_price % 5)
            elif 10000 <= sell_price < 100000:
                adj_sell_price = sell_price - (sell_price % 10)
            elif 100000 <= sell_price < 500000:
                adj_sell_price = sell_price - (sell_price % 50)
            elif 500000 <= sell_price < 1000000:
                adj_sell_price = sell_price - (sell_price % 100)
            elif 1000000 <= sell_price < 2000000:
                adj_sell_price = sell_price - (sell_price % 500)
            elif 2000000 <= sell_price:
                adj_sell_price = sell_price - (sell_price % 1000)

            if float(i['balance']) < 0.01:
                continue
            else:
                print(upbit.sell_limit_order("KRW-" + i['currency'], adj_sell_price, float(i['balance'])))

        #그 특정 시간 e.g. 11:48에 보유주문 전량 취소 후전량 매도

































































