import pyupbit
import pandas
import time

con_key = "g84pSKocX46FRjpSdSmxxyGJ8rV7q5KHpCNVOalx"
sec_key = "SpZmxIuIa4w3xmj3BCCM3Foibaa1xn6n8KDoEOiS"
upbit = pyupbit.Upbit(con_key, sec_key)
tickers = pyupbit.get_tickers(fiat="KRW")

# balance = upbit.get_balances()[0]
# hold_list =[]
# for i in hold_list :
#    hold_list.append(i['currency'])
#
# buy_target = set(tickers) - set(hold_list)
# print(buy_target)
#
# # set(tickers)-


hold_balance = upbit.get_balances()[0]
for i in hold_balance[1:]:
    sell_price =float(i['avg_buy_price'])*1.28
    if sell_price < 10:
        adj_sell_price = format(sell_price, '.2f')
    elif 10<= sell_price <100:
        adj_sell_price = format(sell_price, '.1f')
    elif 100<= sell_price <1000:
        adj_sell_price = round(sell_price)
    elif 1000<= sell_price < 10000:
        adj_sell_price = sell_price - (sell_price % 5)
    elif 10000<= sell_price < 100000:
        adj_sell_price = sell_price - (sell_price % 10)
    elif 100000 <= sell_price < 500000:
        adj_sell_price = sell_price - (sell_price % 50)
    elif 500000 <= sell_price < 1000000:
        adj_sell_price = sell_price - (sell_price % 100)
    elif 1000000 <= sell_price < 2000000:
        adj_sell_price = sell_price - (sell_price % 500)
    elif 2000000<= sell_price:
        adj_sell_price = sell_price - (sell_price % 1000)

    if float(i['balance'])<0.01:
        continue
    else:
        print (i)
        print(adj_sell_price)
        print(i['balance'])
        print(upbit.sell_limit_order("KRW-"+i['currency'], adj_sell_price,float(i['balance'])))
