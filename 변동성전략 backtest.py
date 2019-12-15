import pandas as pd
import datetime
from datetime import timedelta, date
import time
import numpy as np
import pyupbit
import requests


def sell_time_data(ticker, adj_time):  # 특정 매도 시간대 데이터를 붙이는 일
    a = str(date.today() - timedelta(days=1)) + ' ' + adj_time + ':00:00'
    b = datetime.datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
    df_total = []
    #     print(b)
    for i in range(200):
        url = "https://api.upbit.com/v1/candles/minutes/1"
        querystring = {"market": ticker, "to": b, "count": "1"}
        response = requests.request("GET", url, params=querystring)
        data = response.json()
        df_raw = pd.DataFrame(data)
        df_total.append(df_raw)
        b = b - timedelta(days=1)
        time.sleep(0.1)
    df_total = pd.concat(df_total)
    df_total.set_index('candle_date_time_kst', inplace=True)
    price_at_target = df_total.drop(
        columns=['market', 'candle_date_time_utc', 'high_price', 'low_price', 'trade_price', 'timestamp',
                 'candle_acc_trade_price', 'candle_acc_trade_volume', 'unit'])
    price_at_target['norm_index'] = pd.to_datetime(price_at_target.index).normalize()
    price_at_target.set_index('norm_index', inplace=True)
    price_at_target.columns = ['sell_price']

    df = pd.DataFrame(pyupbit.get_ohlcv(ticker))
    df['norm_index'] = pd.to_datetime(df.index).normalize()
    df.set_index('norm_index', inplace=True)

    total_df = df.merge(price_at_target, left_index=True, right_index=True)
    return (total_df)


def get_ror(k):  # 특정 K의 compounding profitability를 계산
    df = total_df
    df['volume_KRW'] = df['volume'] * ((df['open'] + df['high'] + df['close']) / 3)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    fee = 0.0032
    df['ror'] = np.where((df['high'] > df['target']) & (df['volume_KRW'] > 150000000),
                         df['sell_price'] / df['target'] - fee, 1)
    ror = df['ror'].cumprod()[-2]
    #     df.to_excel("/Users/donghyunyoo/Downloads/무제 폴더 2/"+ticker+'.xlsx')
    return ror


tickers = pyupbit.get_tickers('KRW')
# tickers = ['KRW-IGNIS','KRW-XRP']
adj_time = 1  # 01이 10시
for i in range(3):  # 시간을 더해주는 루프
    if len(str(adj_time)) == 1:
        for_time = '0' + str(adj_time)
    else:
        for_time = str(adj_time)
    result = []
    print(for_time, datetime.datetime.now())
    for ticker in tickers:  # 동일한 시간내 여러 코인의 performace를 비교해주는 루프
        ror_dict = {}
        total_df = sell_time_data(ticker, for_time)
        max_ror = 0
        for k in np.arange(0.1, 1, 0.05):
            ror = get_ror(k)
            if ror > max_ror:
                max_ror = ror
                ror_dict[max_ror] = k
            time.sleep(1)
        result_raw = {'ticker': ticker, 'k': ror_dict[max_ror], 'ror': max_ror}
        #         print(result_raw)
        result_data = pd.DataFrame(result_raw, index=[0])
        result.append(result_data)
    #         print(result)
    final_result = pd.concat(result)  # 하나의 시간대에 모든 코인들 퍼포먼스를 하나로 합침
    a = str(date.today() - timedelta(days=1)) + ' ' + str(int(for_time) + 9) + ':00:00'  # 파일명 생성을 위한 라인 from utc to kst
    final_result.to_excel('/Users/donghyunyoo/Downloads/무제 폴더 2/' + a + '.xlsx')
    adj_time = adj_time + 1
print('done')
# 위 펑션을 200으로 바꾼다음에 돌려보기
# 시간도 띄우는게 좋을듯


