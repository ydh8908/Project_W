import pyupbit
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
