import pyupbit
import pandas as pd
import time
import datetime
from pymongo import MongoClient
import json
import requests

# con_key = "g84pSKocX46FRjpSdSmxxyGJ8rV7q5KHpCNVOalx"
# sec_key = "SpZmxIuIa4w3xmj3BCCM3Foibaa1xn6n8KDoEOiS"
# upbit = pyupbit.Upbit(con_key, sec_key)
# tickers = pyupbit.get_tickers(fiat="KRW")

client = MongoClient('localhost', 27017)
db = client.test1

target_time = '2019-09-28 23:41:17'
target_time = datetime.datetime(2019, 9, 28, 23, 41, 17)
his_time =  target_time - datetime.timedelta(minutes=1)
for i in range (2628):
    his_time_for = his_time.strftime('%Y-%m-%d %H:%M:%S')
    print(his_time_for)
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market":"KRW-BTC","to":his_time_for,"count":"200"}
    response = requests.request("GET", url, params=querystring)
    time.sleep(0.1)
    a = response.json()
    for i in range(200):
        find = db.test1.find_one({'market':a[i]['market'], 'candle_date_time_kst':a[i]['candle_date_time_kst']})
        if find is None :
            doc = {
                    'market':a[i]['market'],
                    'candle_date_time_kst':a[i]['candle_date_time_kst'],
                    'opening_price':a[i]['opening_price'],
                    'high_price':a[i]['high_price'],
                    'low_price':a[i]['low_price'],
                    'trade_price':a[i]['trade_price'],
                    'candle_acc_trade_price':a[i]['candle_acc_trade_price'],
                    'candle_acc_trade_volume':a[i]['candle_acc_trade_volume']
                    }
            db.test1.insert_one(doc)
        else :
            continue
    his_time=his_time- datetime.timedelta(minutes=150)