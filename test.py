import pyupbit
import pandas
import time
import datetime

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
now = datetime.datetime.now()
morn_beg = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(hours=11)
morn_end = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(hours=11.002)

print(morn_end)
