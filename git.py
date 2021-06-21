import time
import pyupbit
import datetime
# import numpy
# import numpy.random
import pandas as pd

access_key = "R9RPbdp2ucn95xl8mc4Ah0tp35qfVfJIxLeVUFx9"
secret_key = "2rS6gsl0HSjoRD4x6OGZl15qmUx8xbxgQKN5LZ37"
upbit = pyupbit.Upbit(access_key, secret_key)

trade_wait = []
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

#rsi 공식
def rsi(ohlc: pd.DataFrame, period: int = 14):
    ohlc["close"] = ohlc["close"]
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0
    
    AU = ups.ewm(com = period-1, min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD
    
    return pd.Series(100 - (100/(1 + RS)), name = "RSI")

def get_macd(ticker, short, long, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=365)
    df['ma12'] = df['close'].ewm(span=short).mean()
    df['ma26'] = df['close'].ewm(span=long).mean()
    df["MACD"]=df.apply(lambda x: (x['ma12']-x['ma26']), axis=1)
    df["MACD_signal"]=df["MACD"].ewm(span=k).mean()
    df["MACD_oscillator"]=df.apply(lambda x:(x["MACD"]-x["MACD_signal"]), axis=1)

    return df["MACD_oscillator"]


def get_ma20(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=20)
    ma20 = df['close'].rolling(window=20, min_periods=1).mean().iloc[-1]
    return ma20
    # ma15 = get_ma7("KRW-DOGE") ##실행 코드

def get_ma60(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=60)
    ma60 = df['close'].rolling(window=60, min_periods=1).mean().iloc[-1]
    return ma60
    # ma15 = get_ma20("KRW-DOGE") ##실행 코드

def get_ma120(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=120)
    ma120 = df['close'].rolling(window=120, min_periods=1).mean().iloc[-1]
    return ma120
    # ma15 = get_ma20("KRW-DOGE") ##실행 코드

def get_Envelopes(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=40)
    Envelopes = df['close'].rolling(window=40, min_periods=1).mean().iloc[-1]
    return Envelopes
# def get_Envelopes2(ticker):
#     df = pyupbit.get_ohlcv(ticker, interval="minute1", count=40)
#     Envelopes = df['close'].rolling(window=40, min_periods=1).mean().iloc[-2]
#     return Envelopes

# def get_target_price(ticker, k):
#     """변동성 돌파 전략으로 매수 목표가 조회"""
#     df = pyupbit.get_ohlcv(ticker, interval="minute1", count=50) # 흔적 : 30,
#     k = 1 - abs(df.iloc[0]['open'] - df.iloc[0]['close']) / (df.iloc[0]['high'] - df.iloc[0]['low'])
#     target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
#     return target_price


# def get_start_time(ticker):
#     """시작 시간 조회"""
#     df = pyupbit.get_ohlcv(ticker, interval="minute1", count=1)
#     start_time = df.index[0]
#     return start_time


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

with open("3-1ticker.txt") as f:
    lines = f.readlines()
    ticker1 = lines[0].strip()
    ticker2 = lines[1].strip()
    ticker3 = lines[2].strip()
    ticker4 = lines[3].strip()
    ticker5 = lines[4].strip()
    ticker6 = lines[5].strip()
    ticker7 = lines[6].strip()
    ticker8 = lines[7].strip()
    ticker9 = lines[8].strip()
    ticker10 = lines[9].strip()

print("auto start")

while True:


    now = datetime.datetime.now()
#############################################################################################################
#################################################     1    #################################################
#############################################################################################################
    try:
        krw = get_balance("KRW")
        get1_1 = upbit.get_balance(ticker=ticker1)
        if krw > 5000 and get1_1 < 0.00001:
            data_1 = pyupbit.get_ohlcv(ticker=ticker1, interval="minute1")#(최대 200개까지 요청가능)
            # firstClose_1 = int(data_1.iloc[-2]['close'])# 종가
            firstVolume_1 = int(data_1.iloc[-2]['volume'])# 거래량
            # curClose_1 = int(data_1.iloc[-1]['close'])# 종가
            curVolume_1 = int(data_1.iloc[-1]['volume'])# 거래량
            time.sleep(0.2)

            if (firstVolume_1 * 2.0) < curVolume_1:
                macd1_1 = get_macd(ticker1, 12, 26, 9).iloc[-1]
                time.sleep(0.2)
                macd3_1 = get_macd(ticker1, 48, 14, 9).iloc[-1]
                time.sleep(0.2)
                if macd1_1 > 0 and macd3_1 < 0:
                    Envelopes2_1 = get_Envelopes(ticker1)
                    current_price_1 = get_current_price(ticker1)
                    time.sleep(0.2)
                    if Envelopes2_1 > current_price_1:
                        price_1 = pyupbit.get_current_price(ticker1)
                        time.sleep(0.2)
                        now_rsi_1 = rsi(data_1, 14).iloc[-1]
                        now_rsi2_1 = rsi(data_1, 14).iloc[-2]
                        time.sleep(0.2)
                        current_price_1 = get_current_price(ticker1)
                        time.sleep(0.2)
                        macd2_1 = get_macd(ticker1, 24, 52, 9).iloc[-1]
                        time.sleep(0.2)
                        Envelopes1_1 = get_Envelopes(ticker1) * 0.98
                        time.sleep(0.2)
                        # print("검색 1 완료")
                        ma20_1 = get_ma20(ticker1)
                        ma60_1 = get_ma60(ticker1)
                        ma120_1 = get_ma120(ticker1)
                        time.sleep(0.2)

# 매수
                        if krw > 5000 and get1_1 < 0.00001:
                            if macd1_1 > 0 and macd3_1 < 0 and current_price_1 < Envelopes1_1:

                                ret1 = upbit.buy_limit_order(ticker1, current_price_1, (krw * 0.9995) / current_price_1)
                                uuid1 = ret1['uuid']

                                price1_1 = price_1
                                del macd1_1, macd3_1, data_1, firstVolume_1, curVolume_1, now_rsi_1, now_rsi2_1, current_price_1, macd2_1, Envelopes1_1

                            if now_rsi_1 > now_rsi2_1 and macd1_1 > 0 and (macd1_1 > macd3_1 > macd2_1) and macd3_1 < 0 and (ma20_1 < ma60_1 or ma20_1 < ma120_1) and (ma20_1 > ma60_1 or ma20_1 > ma120_1) and current_price_1 > ma20_1:
                            # if now_rsi_1 > now_rsi2_1 and macd1_1 > 0 and (macd1_1 > macd3_1 > macd2_1) and macd3_1 < 0 and current_price_1 > ma20_1:

                                ret1 = upbit.buy_limit_order(ticker1, current_price_1, (krw * 0.9995) / current_price_1)
                                uuid1 = ret1['uuid']

                                price1_1 = price_1
                                del macd1_1, macd3_1, data_1, firstVolume_1, curVolume_1, now_rsi_1, now_rsi2_1, current_price_1, macd2_1, Envelopes1_1, ma20_1, ma60_1, ma120_1

                        if price1_1 > 1 and get1_1 < 0.00001:
                            if (price1_1 * 0.99) > price_1 or (price1_1 * 1.01) < price_1:

                                ret1 = upbit.cancel_order(uuid1)
                                del uuid1
    except:
        pass


# 매도
    try:
        won1 = pyupbit.get_current_price(ticker1)
        get2_1 = upbit.get_balance(ticker=ticker1)       
        time.sleep(0.2)
    except:
        pass
    try:
        if price1_1 > 1 and get2_1 > 0.00001:
            if won1 > (price1_1 * 1.007):
                ret1_1 = upbit.sell_limit_order(ticker1, won1, get2_1)
                uuid1_1 = ret1_1['uuid']
    except: 
        pass
    try:
        if price1_1 > 1 and get2_1 > 0.00001:
            if won1 < (price1_1 * 0.99):
                ret1_1 = upbit.cancel_order(uuid1_1)
    except: 
        pass
    try:
        if price1_1 > 1 and get2_1 > 0.00001:
            if won1 < (price1_1 * 0.99):
                upbit.sell_market_order(ticker1, get2_1)
                del uuid1_1, get2_1, price1_1, won1
    except: 
        pass
#############################################################################################################
#################################################     2    #################################################
#############################################################################################################
    try:
        krw = get_balance("KRW")
        get1_2 = upbit.get_balance(ticker=ticker2)
        if krw > 5000 and get1_2 < 0.00001:
            data_2 = pyupbit.get_ohlcv(ticker=ticker2, interval="minute1")#(최대 200개까지 요청가능)
            # firstClose_2 = int(data_2.iloc[-2]['close'])# 종가
            firstVolume_2 = int(data_2.iloc[-2]['volume'])# 거래량
            # curClose_2 = int(data_2.iloc[-1]['close'])# 종가
            curVolume_2 = int(data_2.iloc[-1]['volume'])# 거래량
            time.sleep(0.2)

            if (firstVolume_2 * 2.0) < curVolume_2:
                macd1_2 = get_macd(ticker2, 12, 26, 9).iloc[-1]
                time.sleep(0.2)
                macd3_2 = get_macd(ticker2, 48, 24, 9).iloc[-1]
                time.sleep(0.2)
                if macd1_2 > 0 and macd3_2 < 0:
                    Envelopes2_2 = get_Envelopes(ticker2)
                    current_price_2 = get_current_price(ticker2)
                    time.sleep(0.2)
                    if Envelopes2_2 > current_price_2:
                        price_2 = pyupbit.get_current_price(ticker2)
                        time.sleep(0.2)
                        now_rsi_2 = rsi(data_2, 14).iloc[-1]
                        now_rsi2_2 = rsi(data_2, 14).iloc[-2]
                        time.sleep(0.2)
                        current_price_2 = get_current_price(ticker2)
                        time.sleep(0.2)
                        macd2_2 = get_macd(ticker2, 24, 52, 9).iloc[-1]
                        time.sleep(0.2)
                        Envelopes1_2 = get_Envelopes(ticker2) * 0.98
                        time.sleep(0.2)
                        # print("검색 2 완료")
                        ma20_2 = get_ma20(ticker2)
                        ma60_2 = get_ma60(ticker2)
                        ma120_2 = get_ma120(ticker2)
                        time.sleep(0.2)

# 매수
                        if krw > 5000 and get1_2 < 0.00001:
                            if macd1_2 > 0 and macd3_2 < 0 and current_price_2 < Envelopes1_2:

                                ret2 = upbit.buy_limit_order(ticker2, current_price_2, (krw * 0.9995) / current_price_2)
                                uuid2 = ret2['uuid']

                                price1_2 = price_2
                                del macd1_2, macd3_2, data_2, firstVolume_2, curVolume_2, now_rsi_2, now_rsi2_2, current_price_2, macd2_2, Envelopes1_2

                            if now_rsi_2 > now_rsi2_2 and macd1_2 > 0 and (macd1_2 > macd3_2 > macd2_2) and macd3_2 < 0 and (ma20_2 < ma60_2 or ma20_2 < ma120_2) and (ma20_2 > ma60_2 or ma20_2 > ma120_2) and current_price_2 > ma20_2:
                            # if now_rsi_2 > now_rsi2_2 and macd1_2 > 0 and (macd1_2 > macd3_2 > macd2_2) and macd3_2 < 0 and current_price_2 > ma20_2:

                                ret2 = upbit.buy_limit_order(ticker2, current_price_2, (krw * 0.9995) / current_price_2)
                                uuid2 = ret2['uuid']

                                price1_2 = price_2
                                del macd1_2, macd3_2, data_2, firstVolume_2, curVolume_2, now_rsi_2, now_rsi2_2, current_price_2, macd2_2, Envelopes1_2, ma20_2, ma60_2, ma120_2

                        if price1_2 > 1 and get1_2 < 0.00001:
                            if (price1_2 * 0.99) > price_2 or (price1_2 * 1.01) < price_2:

                                ret2 = upbit.cancel_order(uuid2)
                                del uuid2
    except:
        pass


# 매도
    try:
        won2 = pyupbit.get_current_price(ticker2)
        get2_2 = upbit.get_balance(ticker=ticker2)       
        time.sleep(0.2)
    except:
        pass
    try:
        if price1_2 > 1 and get2_2 > 0.00001:
            if won2 > (price1_2 * 1.007):
                ret2_2 = upbit.sell_limit_order(ticker2, won2, get2_2)
                uuid2_2 = ret2_2['uuid']
    except: 
        pass
    try:
        if price1_2 > 1 and get2_2 > 0.00001:
            if won2 < (price1_2 * 0.99):
                ret2_2 = upbit.cancel_order(uuid2_2)
    except: 
        pass
    try:
        if price1_2 > 1 and get2_2 > 0.00001:
            if won2 < (price1_2 * 0.99):
                upbit.sell_market_order(ticker2, get2_2)
                del uuid2_2, get2_2, price1_2, won2
    except: 
        pass
#############################################################################################################
#################################################     3    #################################################
#############################################################################################################
    try:
        krw = get_balance("KRW")
        get1_3 = upbit.get_balance(ticker=ticker3)
        if krw > 5000 and get1_3 < 0.00001:
            data_3 = pyupbit.get_ohlcv(ticker=ticker3, interval="minute1")#(최대 200개까지 요청가능)
            # firstClose_3 = int(data_3.iloc[-2]['close'])# 종가
            firstVolume_3 = int(data_3.iloc[-2]['volume'])# 거래량
            # curClose_3 = int(data_3.iloc[-1]['close'])# 종가
            curVolume_3 = int(data_3.iloc[-1]['volume'])# 거래량
            time.sleep(0.2)

            if (firstVolume_3 * 2.0) < curVolume_3:
                macd1_3 = get_macd(ticker3, 12, 26, 9).iloc[-1]
                time.sleep(0.2)
                macd3_3 = get_macd(ticker3, 48, 34, 9).iloc[-1]
                time.sleep(0.2)
                if macd1_3 > 0 and macd3_3 < 0:
                    Envelopes2_3 = get_Envelopes(ticker3)
                    current_price_3 = get_current_price(ticker3)
                    time.sleep(0.2)
                    if Envelopes2_3 > current_price_3:
                        price_3 = pyupbit.get_current_price(ticker3)
                        time.sleep(0.2)
                        now_rsi_3 = rsi(data_3, 14).iloc[-1]
                        now_rsi2_3 = rsi(data_3, 14).iloc[-2]
                        time.sleep(0.2)
                        current_price_3 = get_current_price(ticker3)
                        time.sleep(0.2)
                        macd2_3 = get_macd(ticker3, 24, 52, 9).iloc[-1]
                        time.sleep(0.2)
                        Envelopes1_3 = get_Envelopes(ticker3) * 0.98
                        time.sleep(0.2)
                        # print("검색 3 완료")
                        ma20_3 = get_ma20(ticker3)
                        ma60_3 = get_ma60(ticker3)
                        ma120_3 = get_ma120(ticker3)
                        time.sleep(0.2)

# 매수
                        if krw > 5000 and get1_3 < 0.00001:
                            if macd1_3 > 0 and macd3_3 < 0 and current_price_3 < Envelopes1_3:

                                ret3 = upbit.buy_limit_order(ticker3, current_price_3, (krw * 0.9995) / current_price_3)
                                uuid3 = ret3['uuid']

                                price1_3 = price_3
                                del macd1_3, macd3_3, data_3, firstVolume_3, curVolume_3, now_rsi_3, now_rsi2_3, current_price_3, macd2_3, Envelopes1_3

                            if now_rsi_3 > now_rsi2_3 and macd1_3 > 0 and (macd1_3 > macd3_3 > macd2_3) and macd3_3 < 0 and (ma20_3 < ma60_3 or ma20_3 < ma120_3) and (ma20_3 > ma60_3 or ma20_3 > ma120_3) and current_price_3 > ma20_3:
                            # if now_rsi_3 > now_rsi2_3 and macd1_3 > 0 and (macd1_3 > macd3_3 > macd2_3) and macd3_3 < 0 and current_price_3 > ma20_3:

                                ret3 = upbit.buy_limit_order(ticker3, current_price_3, (krw * 0.9995) / current_price_3)
                                uuid3 = ret3['uuid']

                                price1_3 = price_3
                                del macd1_3, macd3_3, data_3, firstVolume_3, curVolume_3, now_rsi_3, now_rsi2_3, current_price_3, macd2_3, Envelopes1_3, ma20_3, ma60_3, ma120_3

                        if price1_3 > 1 and get1_3 < 0.00001:
                            if (price1_3 * 0.99) > price_3 or (price1_3 * 1.01) < price_3:

                                ret3 = upbit.cancel_order(uuid3)
                                del uuid3
    except:
        pass


# 매도
    try:
        won3 = pyupbit.get_current_price(ticker3)
        get2_3 = upbit.get_balance(ticker=ticker3)       
        time.sleep(0.2)
    except:
        pass
    try:
        if price1_3 > 1 and get2_3 > 0.00001:
            if won3 > (price1_3 * 1.007):
                ret3_3 = upbit.sell_limit_order(ticker3, won3, get2_3)
                uuid3_3 = ret3_3['uuid']
    except: 
        pass
    try:
        if price1_3 > 1 and get2_3 > 0.00001:
            if won3 < (price1_3 * 0.99):
                ret3_3 = upbit.cancel_order(uuid3_3)
    except: 
        pass
    try:
        if price1_3 > 1 and get2_3 > 0.00001:
            if won3 < (price1_3 * 0.99):
                upbit.sell_market_order(ticker3, get2_3)
                del uuid3_3, get2_3, price1_3, won3
    except: 
        pass
#############################################################################################################
#################################################     4    #################################################
#############################################################################################################
    try:
        krw = get_balance("KRW")
        get1_4 = upbit.get_balance(ticker=ticker4)
        if krw > 5000 and get1_4 < 0.00001:
            data_4 = pyupbit.get_ohlcv(ticker=ticker4, interval="minute1")#(최대 200개까지 요청가능)
            # firstClose_4 = int(data_4.iloc[-2]['close'])# 종가
            firstVolume_4 = int(data_4.iloc[-2]['volume'])# 거래량
            # curClose_4 = int(data_4.iloc[-1]['close'])# 종가
            curVolume_4 = int(data_4.iloc[-1]['volume'])# 거래량
            time.sleep(0.2)

            if (firstVolume_4 * 2.0) < curVolume_4:
                macd1_4 = get_macd(ticker4, 12, 26, 9).iloc[-1]
                time.sleep(0.2)
                macd3_4 = get_macd(ticker4, 48, 44, 9).iloc[-1]
                time.sleep(0.2)
                if macd1_4 > 0 and macd3_4 < 0:
                    Envelopes2_4 = get_Envelopes(ticker4)
                    current_price_4 = get_current_price(ticker4)
                    time.sleep(0.2)
                    if Envelopes2_4 > current_price_4:
                        price_4 = pyupbit.get_current_price(ticker4)
                        time.sleep(0.2)
                        now_rsi_4 = rsi(data_4, 14).iloc[-1]
                        now_rsi2_4 = rsi(data_4, 14).iloc[-2]
                        time.sleep(0.2)
                        current_price_4 = get_current_price(ticker4)
                        time.sleep(0.2)
                        macd2_4 = get_macd(ticker4, 24, 52, 9).iloc[-1]
                        time.sleep(0.2)
                        Envelopes1_4 = get_Envelopes(ticker4) * 0.98
                        time.sleep(0.2)
                        # print("검색 4 완료")
                        ma20_4 = get_ma20(ticker4)
                        ma60_4 = get_ma60(ticker4)
                        ma120_4 = get_ma120(ticker4)
                        time.sleep(0.2)

# 매수
                        if krw > 5000 and get1_4 < 0.00001:
                            if macd1_4 > 0 and macd3_4 < 0 and current_price_4 < Envelopes1_4:

                                ret4 = upbit.buy_limit_order(ticker4, current_price_4, (krw * 0.9995) / current_price_4)
                                uuid4 = ret4['uuid']

                                price1_4 = price_4
                                del macd1_4, macd3_4, data_4, firstVolume_4, curVolume_4, now_rsi_4, now_rsi2_4, current_price_4, macd2_4, Envelopes1_4

                            if now_rsi_4 > now_rsi2_4 and macd1_4 > 0 and (macd1_4 > macd3_4 > macd2_4) and macd3_4 < 0 and (ma20_4 < ma60_4 or ma20_4 < ma120_4) and (ma20_4 > ma60_4 or ma20_4 > ma120_4) and current_price_4 > ma20_4:
                            # if now_rsi_4 > now_rsi2_4 and macd1_4 > 0 and (macd1_4 > macd3_4 > macd2_4) and macd3_4 < 0 and current_price_4 > ma20_4:

                                ret4 = upbit.buy_limit_order(ticker4, current_price_4, (krw * 0.9995) / current_price_4)
                                uuid4 = ret4['uuid']

                                price1_4 = price_4
                                del macd1_4, macd3_4, data_4, firstVolume_4, curVolume_4, now_rsi_4, now_rsi2_4, current_price_4, macd2_4, Envelopes1_4, ma20_4, ma60_4, ma120_4

                        if price1_4 > 1 and get1_4 < 0.00001:
                            if (price1_4 * 0.99) > price_4 or (price1_4 * 1.01) < price_4:

                                ret4 = upbit.cancel_order(uuid4)
                                del uuid4
    except:
        pass


# 매도
    try:
        won4 = pyupbit.get_current_price(ticker4)
        get2_4 = upbit.get_balance(ticker=ticker4)       
        time.sleep(0.2)
    except:
        pass
    try:
        if price1_4 > 1 and get2_4 > 0.00001:
            if won4 > (price1_4 * 1.007):
                ret4_4 = upbit.sell_limit_order(ticker4, won4, get2_4)
                uuid4_4 = ret4_4['uuid']
    except: 
        pass
    try:
        if price1_4 > 1 and get2_4 > 0.00001:
            if won4 < (price1_4 * 0.99):
                ret4_4 = upbit.cancel_order(uuid4_4)
    except: 
        pass
    try:
        if price1_4 > 1 and get2_4 > 0.00001:
            if won4 < (price1_4 * 0.99):
                upbit.sell_market_order(ticker4, get2_4)
                del uuid4_4, get2_4, price1_4, won4
    except: 
        pass
#############################################################################################################
#################################################     5    #################################################
#############################################################################################################
    try:
        krw = get_balance("KRW")
        get1_5 = upbit.get_balance(ticker=ticker5)
        if krw > 5000 and get1_5 < 0.00001:
            data_5 = pyupbit.get_ohlcv(ticker=ticker5, interval="minute1")#(최대 200개까지 요청가능)
            # firstClose_5 = int(data_5.iloc[-2]['close'])# 종가
            firstVolume_5 = int(data_5.iloc[-2]['volume'])# 거래량
            # curClose_5 = int(data_5.iloc[-1]['close'])# 종가
            curVolume_5 = int(data_5.iloc[-1]['volume'])# 거래량
            time.sleep(0.2)

            if (firstVolume_5 * 2.0) < curVolume_5:
                macd1_5 = get_macd(ticker5, 12, 26, 9).iloc[-1]
                time.sleep(0.2)
                macd3_5 = get_macd(ticker5, 48, 54, 9).iloc[-1]
                time.sleep(0.2)
                if macd1_5 > 0 and macd3_5 < 0:
                    Envelopes2_5 = get_Envelopes(ticker5)
                    current_price_5 = get_current_price(ticker5)
                    time.sleep(0.2)
                    if Envelopes2_5 > current_price_5:
                        price_5 = pyupbit.get_current_price(ticker5)
                        time.sleep(0.2)
                        now_rsi_5 = rsi(data_5, 14).iloc[-1]
                        now_rsi2_5 = rsi(data_5, 14).iloc[-2]
                        time.sleep(0.2)
                        current_price_5 = get_current_price(ticker5)
                        time.sleep(0.2)
                        macd2_5 = get_macd(ticker5, 24, 52, 9).iloc[-1]
                        time.sleep(0.2)
                        Envelopes1_5 = get_Envelopes(ticker5) * 0.98
                        time.sleep(0.2)
                        # print("검색 5 완료")
                        ma20_5 = get_ma20(ticker5)
                        ma60_5 = get_ma60(ticker5)
                        ma120_5 = get_ma120(ticker5)
                        time.sleep(0.2)

# 매수
                        if krw > 5000 and get1_5 < 0.00001:
                            if macd1_5 > 0 and macd3_5 < 0 and current_price_5 < Envelopes1_5:

                                ret5 = upbit.buy_limit_order(ticker5, current_price_5, (krw * 0.9995) / current_price_5)
                                uuid5 = ret5['uuid']

                                price1_5 = price_5
                                del macd1_5, macd3_5, data_5, firstVolume_5, curVolume_5, now_rsi_5, now_rsi2_5, current_price_5, macd2_5, Envelopes1_5

                            if now_rsi_5 > now_rsi2_5 and macd1_5 > 0 and (macd1_5 > macd3_5 > macd2_5) and macd3_5 < 0 and (ma20_5 < ma60_5 or ma20_5 < ma120_5) and (ma20_5 > ma60_5 or ma20_5 > ma120_5) and current_price_5 > ma20_5:
                            # if now_rsi_5 > now_rsi2_5 and macd1_5 > 0 and (macd1_5 > macd3_5 > macd2_5) and macd3_5 < 0 and current_price_5 > ma20_5:

                                ret5 = upbit.buy_limit_order(ticker5, current_price_5, (krw * 0.9995) / current_price_5)
                                uuid5 = ret5['uuid']

                                price1_5 = price_5
                                del macd1_5, macd3_5, data_5, firstVolume_5, curVolume_5, now_rsi_5, now_rsi2_5, current_price_5, macd2_5, Envelopes1_5, ma20_5, ma60_5, ma120_5

                        if price1_5 > 1 and get1_5 < 0.00001:
                            if (price1_5 * 0.99) > price_5 or (price1_5 * 1.01) < price_5:

                                ret5 = upbit.cancel_order(uuid5)
                                del uuid5
    except:
        pass


# 매도
    try:
        won5 = pyupbit.get_current_price(ticker5)
        get2_5 = upbit.get_balance(ticker=ticker5)       
        time.sleep(0.2)
    except:
        pass
    try:
        if price1_5 > 1 and get2_5 > 0.00001:
            if won5 > (price1_5 * 1.007):
                ret5_5 = upbit.sell_limit_order(ticker5, won5, get2_5)
                uuid5_5 = ret5_5['uuid']
    except: 
        pass
    try:
        if price1_5 > 1 and get2_5 > 0.00001:
            if won5 < (price1_5 * 0.99):
                ret5_5 = upbit.cancel_order(uuid5_5)
    except: 
        pass
    try:
        if price1_5 > 1 and get2_5 > 0.00001:
            if won5 < (price1_5 * 0.99):
                upbit.sell_market_order(ticker5, get2_5)
                del uuid5_5, get2_5, price1_5, won5
    except: 
        pass
#############################################################################################################
#################################################     6    #################################################
#############################################################################################################
    try:
        krw = get_balance("KRW")
        get1_6 = upbit.get_balance(ticker=ticker6)
        if krw > 5000 and get1_6 < 0.00001:
            data_6 = pyupbit.get_ohlcv(ticker=ticker6, interval="minute1")#(최대 200개까지 요청가능)
            # firstClose_6 = int(data_6.iloc[-2]['close'])# 종가
            firstVolume_6 = int(data_6.iloc[-2]['volume'])# 거래량
            # curClose_6 = int(data_6.iloc[-1]['close'])# 종가
            curVolume_6 = int(data_6.iloc[-1]['volume'])# 거래량
            time.sleep(0.2)

            if (firstVolume_6 * 2.0) < curVolume_6:
                macd1_6 = get_macd(ticker6, 12, 26, 9).iloc[-1]
                time.sleep(0.2)
                macd3_6 = get_macd(ticker6, 48, 64, 9).iloc[-1]
                time.sleep(0.2)
                if macd1_6 > 0 and macd3_6 < 0:
                    Envelopes2_6 = get_Envelopes(ticker6)
                    current_price_6 = get_current_price(ticker6)
                    time.sleep(0.2)
                    if Envelopes2_6 > current_price_6:
                        price_6 = pyupbit.get_current_price(ticker6)
                        time.sleep(0.2)
                        now_rsi_6 = rsi(data_6, 14).iloc[-1]
                        now_rsi2_6 = rsi(data_6, 14).iloc[-2]
                        time.sleep(0.2)
                        current_price_6 = get_current_price(ticker6)
                        time.sleep(0.2)
                        macd2_6 = get_macd(ticker6, 24, 52, 9).iloc[-1]
                        time.sleep(0.2)
                        Envelopes1_6 = get_Envelopes(ticker6) * 0.98
                        time.sleep(0.2)
                        # print("검색 6 완료")
                        ma20_6 = get_ma20(ticker6)
                        ma60_6 = get_ma60(ticker6)
                        ma120_6 = get_ma120(ticker6)
                        time.sleep(0.2)

# 매수
                        if krw > 5000 and get1_6 < 0.00001:
                            if macd1_6 > 0 and macd3_6 < 0 and current_price_6 < Envelopes1_6:

                                ret6 = upbit.buy_limit_order(ticker6, current_price_6, (krw * 0.9995) / current_price_6)
                                uuid6 = ret6['uuid']

                                price1_6 = price_6
                                del macd1_6, macd3_6, data_6, firstVolume_6, curVolume_6, now_rsi_6, now_rsi2_6, current_price_6, macd2_6, Envelopes1_6

                            if now_rsi_6 > now_rsi2_6 and macd1_6 > 0 and (macd1_6 > macd3_6 > macd2_6) and macd3_6 < 0 and (ma20_6 < ma60_6 or ma20_6 < ma120_6) and (ma20_6 > ma60_6 or ma20_6 > ma120_6) and current_price_6 > ma20_6:
                            # if now_rsi_6 > now_rsi2_6 and macd1_6 > 0 and (macd1_6 > macd3_6 > macd2_6) and macd3_6 < 0 and current_price_6 > ma20_6:

                                ret6 = upbit.buy_limit_order(ticker6, current_price_6, (krw * 0.9995) / current_price_6)
                                uuid6 = ret6['uuid']

                                price1_6 = price_6
                                del macd1_6, macd3_6, data_6, firstVolume_6, curVolume_6, now_rsi_6, now_rsi2_6, current_price_6, macd2_6, Envelopes1_6, ma20_6, ma60_6, ma120_6

                        if price1_6 > 1 and get1_6 < 0.00001:
                            if (price1_6 * 0.99) > price_6 or (price1_6 * 1.01) < price_6:

                                ret6 = upbit.cancel_order(uuid6)
                                del uuid6
    except:
        pass


# 매도
    try:
        won6 = pyupbit.get_current_price(ticker6)
        get2_6 = upbit.get_balance(ticker=ticker6)       
        time.sleep(0.2)
    except:
        pass
    try:
        if price1_6 > 1 and get2_6 > 0.00001:
            if won6 > (price1_6 * 1.007):
                ret6_6 = upbit.sell_limit_order(ticker6, won6, get2_6)
                uuid6_6 = ret6_6['uuid']
    except: 
        pass
    try:
        if price1_6 > 1 and get2_6 > 0.00001:
            if won6 < (price1_6 * 0.99):
                ret6_6 = upbit.cancel_order(uuid6_6)
    except: 
        pass
    try:
        if price1_6 > 1 and get2_6 > 0.00001:
            if won6 < (price1_6 * 0.99):
                upbit.sell_market_order(ticker6, get2_6)
                del uuid6_6, get2_6, price1_6, won6
    except: 
        pass
#############################################################################################################
#################################################     7    #################################################
#############################################################################################################
    try:
        krw = get_balance("KRW")
        get1_7 = upbit.get_balance(ticker=ticker7)
        if krw > 5000 and get1_7 < 0.00001:
            data_7 = pyupbit.get_ohlcv(ticker=ticker7, interval="minute1")#(최대 200개까지 요청가능)
            # firstClose_7 = int(data_7.iloc[-2]['close'])# 종가
            firstVolume_7 = int(data_7.iloc[-2]['volume'])# 거래량
            # curClose_7 = int(data_7.iloc[-1]['close'])# 종가
            curVolume_7 = int(data_7.iloc[-1]['volume'])# 거래량
            time.sleep(0.2)

            if (firstVolume_7 * 2.0) < curVolume_7:
                macd1_7 = get_macd(ticker7, 12, 26, 9).iloc[-1]
                time.sleep(0.2)
                macd3_7 = get_macd(ticker7, 48, 74, 9).iloc[-1]
                time.sleep(0.2)
                if macd1_7 > 0 and macd3_7 < 0:
                    Envelopes2_7 = get_Envelopes(ticker7)
                    current_price_7 = get_current_price(ticker7)
                    time.sleep(0.2)
                    if Envelopes2_7 > current_price_7:
                        price_7 = pyupbit.get_current_price(ticker7)
                        time.sleep(0.2)
                        now_rsi_7 = rsi(data_7, 14).iloc[-1]
                        now_rsi2_7 = rsi(data_7, 14).iloc[-2]
                        time.sleep(0.2)
                        current_price_7 = get_current_price(ticker7)
                        time.sleep(0.2)
                        macd2_7 = get_macd(ticker7, 24, 52, 9).iloc[-1]
                        time.sleep(0.2)
                        Envelopes1_7 = get_Envelopes(ticker7) * 0.98
                        time.sleep(0.2)
                        # print("검색 7 완료")
                        ma20_7 = get_ma20(ticker7)
                        ma60_7 = get_ma60(ticker7)
                        ma120_7 = get_ma120(ticker7)
                        time.sleep(0.2)

# 매수
                        if krw > 5000 and get1_7 < 0.00001:
                            if macd1_7 > 0 and macd3_7 < 0 and current_price_7 < Envelopes1_7:

                                ret7 = upbit.buy_limit_order(ticker7, current_price_7, (krw * 0.9995) / current_price_7)
                                uuid7 = ret7['uuid']

                                price1_7 = price_7
                                del macd1_7, macd3_7, data_7, firstVolume_7, curVolume_7, now_rsi_7, now_rsi2_7, current_price_7, macd2_7, Envelopes1_7

                            if now_rsi_7 > now_rsi2_7 and macd1_7 > 0 and (macd1_7 > macd3_7 > macd2_7) and macd3_7 < 0 and (ma20_7 < ma60_7 or ma20_7 < ma120_7) and (ma20_7 > ma60_7 or ma20_7 > ma120_7) and current_price_7 > ma20_7:
                            # if now_rsi_7 > now_rsi2_7 and macd1_7 > 0 and (macd1_7 > macd3_7 > macd2_7) and macd3_7 < 0 and current_price_7 > ma20_7:

                                ret7 = upbit.buy_limit_order(ticker7, current_price_7, (krw * 0.9995) / current_price_7)
                                uuid7 = ret7['uuid']

                                price1_7 = price_7
                                del macd1_7, macd3_7, data_7, firstVolume_7, curVolume_7, now_rsi_7, now_rsi2_7, current_price_7, macd2_7, Envelopes1_7, ma20_7, ma60_7, ma120_7

                        if price1_7 > 1 and get1_7 < 0.00001:
                            if (price1_7 * 0.99) > price_7 or (price1_7 * 1.01) < price_7:

                                ret7 = upbit.cancel_order(uuid7)
                                del uuid7
    except:
        pass


# 매도
    try:
        won7 = pyupbit.get_current_price(ticker7)
        get2_7 = upbit.get_balance(ticker=ticker7)       
        time.sleep(0.2)
    except:
        pass
    try:
        if price1_7 > 1 and get2_7 > 0.00001:
            if won7 > (price1_7 * 1.007):
                ret7_7 = upbit.sell_limit_order(ticker7, won7, get2_7)
                uuid7_7 = ret7_7['uuid']
    except: 
        pass
    try:
        if price1_7 > 1 and get2_7 > 0.00001:
            if won7 < (price1_7 * 0.99):
                ret7_7 = upbit.cancel_order(uuid7_7)
    except: 
        pass
    try:
        if price1_7 > 1 and get2_7 > 0.00001:
            if won7 < (price1_7 * 0.99):
                upbit.sell_market_order(ticker7, get2_7)
                del uuid7_7, get2_7, price1_7, won7
    except: 
        pass
#############################################################################################################
#################################################     8    #################################################
#############################################################################################################
    try:
        krw = get_balance("KRW")
        get1_8 = upbit.get_balance(ticker=ticker8)
        if krw > 5000 and get1_8 < 0.00001:
            data_8 = pyupbit.get_ohlcv(ticker=ticker8, interval="minute1")#(최대 200개까지 요청가능)
            # firstClose_8 = int(data_8.iloc[-2]['close'])# 종가
            firstVolume_8 = int(data_8.iloc[-2]['volume'])# 거래량
            # curClose_8 = int(data_8.iloc[-1]['close'])# 종가
            curVolume_8 = int(data_8.iloc[-1]['volume'])# 거래량
            time.sleep(0.2)

            if (firstVolume_8 * 2.0) < curVolume_8:
                macd1_8 = get_macd(ticker8, 12, 26, 9).iloc[-1]
                time.sleep(0.2)
                macd3_8 = get_macd(ticker8, 48, 84, 9).iloc[-1]
                time.sleep(0.2)
                if macd1_8 > 0 and macd3_8 < 0:
                    Envelopes2_8 = get_Envelopes(ticker8)
                    current_price_8 = get_current_price(ticker8)
                    time.sleep(0.2)
                    if Envelopes2_8 > current_price_8:
                        price_8 = pyupbit.get_current_price(ticker8)
                        time.sleep(0.2)
                        now_rsi_8 = rsi(data_8, 14).iloc[-1]
                        now_rsi2_8 = rsi(data_8, 14).iloc[-2]
                        time.sleep(0.2)
                        current_price_8 = get_current_price(ticker8)
                        time.sleep(0.2)
                        macd2_8 = get_macd(ticker8, 24, 52, 9).iloc[-1]
                        time.sleep(0.2)
                        Envelopes1_8 = get_Envelopes(ticker8) * 0.98
                        time.sleep(0.2)
                        # print("검색 8 완료")
                        ma20_8 = get_ma20(ticker8)
                        ma60_8 = get_ma60(ticker8)
                        ma120_8 = get_ma120(ticker8)
                        time.sleep(0.2)

# 매수
                        if krw > 5000 and get1_8 < 0.00001:
                            if macd1_8 > 0 and macd3_8 < 0 and current_price_8 < Envelopes1_8:

                                ret8 = upbit.buy_limit_order(ticker8, current_price_8, (krw * 0.9995) / current_price_8)
                                uuid8 = ret8['uuid']

                                price1_8 = price_8
                                del macd1_8, macd3_8, data_8, firstVolume_8, curVolume_8, now_rsi_8, now_rsi2_8, current_price_8, macd2_8, Envelopes1_8

                            if now_rsi_8 > now_rsi2_8 and macd1_8 > 0 and (macd1_8 > macd3_8 > macd2_8) and macd3_8 < 0 and (ma20_8 < ma60_8 or ma20_8 < ma120_8) and (ma20_8 > ma60_8 or ma20_8 > ma120_8) and current_price_8 > ma20_8:
                            # if now_rsi_8 > now_rsi2_8 and macd1_8 > 0 and (macd1_8 > macd3_8 > macd2_8) and macd3_8 < 0 and current_price_8 > ma20_8:

                                ret8 = upbit.buy_limit_order(ticker8, current_price_8, (krw * 0.9995) / current_price_8)
                                uuid8 = ret8['uuid']

                                price1_8 = price_8
                                del macd1_8, macd3_8, data_8, firstVolume_8, curVolume_8, now_rsi_8, now_rsi2_8, current_price_8, macd2_8, Envelopes1_8, ma20_8, ma60_8, ma120_8

                        if price1_8 > 1 and get1_8 < 0.00001:
                            if (price1_8 * 0.99) > price_8 or (price1_8 * 1.01) < price_8:

                                ret8 = upbit.cancel_order(uuid8)
                                del uuid8
    except:
        pass


# 매도
    try:
        won8 = pyupbit.get_current_price(ticker8)
        get2_8 = upbit.get_balance(ticker=ticker8)       
        time.sleep(0.2)
    except:
        pass
    try:
        if price1_8 > 1 and get2_8 > 0.00001:
            if won8 > (price1_8 * 1.007):
                ret8_8 = upbit.sell_limit_order(ticker8, won8, get2_8)
                uuid8_8 = ret8_8['uuid']
    except: 
        pass
    try:
        if price1_8 > 1 and get2_8 > 0.00001:
            if won8 < (price1_8 * 0.99):
                ret8_8 = upbit.cancel_order(uuid8_8)
    except: 
        pass
    try:
        if price1_8 > 1 and get2_8 > 0.00001:
            if won8 < (price1_8 * 0.99):
                upbit.sell_market_order(ticker8, get2_8)
                del uuid8_8, get2_8, price1_8, won8
    except: 
        pass
#############################################################################################################
#################################################     9    #################################################
#############################################################################################################
    try:
        krw = get_balance("KRW")
        get1_9 = upbit.get_balance(ticker=ticker9)
        if krw > 5000 and get1_9 < 0.00001:
            data_9 = pyupbit.get_ohlcv(ticker=ticker9, interval="minute1")#(최대 200개까지 요청가능)
            # firstClose_9 = int(data_9.iloc[-2]['close'])# 종가
            firstVolume_9 = int(data_9.iloc[-2]['volume'])# 거래량
            # curClose_9 = int(data_9.iloc[-1]['close'])# 종가
            curVolume_9 = int(data_9.iloc[-1]['volume'])# 거래량
            time.sleep(0.2)

            if (firstVolume_9 * 2.0) < curVolume_9:
                macd1_9 = get_macd(ticker9, 12, 26, 9).iloc[-1]
                time.sleep(0.2)
                macd3_9 = get_macd(ticker9, 48, 94, 9).iloc[-1]
                time.sleep(0.2)
                if macd1_9 > 0 and macd3_9 < 0:
                    Envelopes2_9 = get_Envelopes(ticker9)
                    current_price_9 = get_current_price(ticker9)
                    time.sleep(0.2)
                    if Envelopes2_9 > current_price_9:
                        price_9 = pyupbit.get_current_price(ticker9)
                        time.sleep(0.2)
                        now_rsi_9 = rsi(data_9, 14).iloc[-1]
                        now_rsi2_9 = rsi(data_9, 14).iloc[-2]
                        time.sleep(0.2)
                        current_price_9 = get_current_price(ticker9)
                        time.sleep(0.2)
                        macd2_9 = get_macd(ticker9, 24, 52, 9).iloc[-1]
                        time.sleep(0.2)
                        Envelopes1_9 = get_Envelopes(ticker9) * 0.98
                        time.sleep(0.2)
                        # print("검색 9 완료")
                        ma20_9 = get_ma20(ticker9)
                        ma60_9 = get_ma60(ticker9)
                        ma120_9 = get_ma120(ticker9)
                        time.sleep(0.2)

# 매수
                        if krw > 5000 and get1_9 < 0.00001:
                            if macd1_9 > 0 and macd3_9 < 0 and current_price_9 < Envelopes1_9:

                                ret9 = upbit.buy_limit_order(ticker9, current_price_9, (krw * 0.9995) / current_price_9)
                                uuid9 = ret9['uuid']

                                price1_9 = price_9
                                del macd1_9, macd3_9, data_9, firstVolume_9, curVolume_9, now_rsi_9, now_rsi2_9, current_price_9, macd2_9, Envelopes1_9

                            if now_rsi_9 > now_rsi2_9 and macd1_9 > 0 and (macd1_9 > macd3_9 > macd2_9) and macd3_9 < 0 and (ma20_9 < ma60_9 or ma20_9 < ma120_9) and (ma20_9 > ma60_9 or ma20_9 > ma120_9) and current_price_9 > ma20_9:
                            # if now_rsi_9 > now_rsi2_9 and macd1_9 > 0 and (macd1_9 > macd3_9 > macd2_9) and macd3_9 < 0 and current_price_9 > ma20_9:

                                ret9 = upbit.buy_limit_order(ticker9, current_price_9, (krw * 0.9995) / current_price_9)
                                uuid9 = ret9['uuid']

                                price1_9 = price_9
                                del macd1_9, macd3_9, data_9, firstVolume_9, curVolume_9, now_rsi_9, now_rsi2_9, current_price_9, macd2_9, Envelopes1_9, ma20_9, ma60_9, ma120_9

                        if price1_9 > 1 and get1_9 < 0.00001:
                            if (price1_9 * 0.99) > price_9 or (price1_9 * 1.01) < price_9:

                                ret9 = upbit.cancel_order(uuid9)
                                del uuid9
    except:
        pass


# 매도
    try:
        won9 = pyupbit.get_current_price(ticker9)
        get2_9 = upbit.get_balance(ticker=ticker9)       
        time.sleep(0.2)
    except:
        pass
    try:
        if price1_9 > 1 and get2_9 > 0.00001:
            if won9 > (price1_9 * 1.007):
                ret9_9 = upbit.sell_limit_order(ticker9, won9, get2_9)
                uuid9_9 = ret9_9['uuid']
    except: 
        pass
    try:
        if price1_9 > 1 and get2_9 > 0.00001:
            if won9 < (price1_9 * 0.99):
                ret9_9 = upbit.cancel_order(uuid9_9)
    except: 
        pass
    try:
        if price1_9 > 1 and get2_9 > 0.00001:
            if won9 < (price1_9 * 0.99):
                upbit.sell_market_order(ticker9, get2_9)
                del uuid9_9, get2_9, price1_9, won9
    except: 
        pass
#############################################################################################################
#################################################     10    #################################################
#############################################################################################################
    try:
        krw = get_balance("KRW")
        get1_10 = upbit.get_balance(ticker=ticker10)
        if krw > 5000 and get1_10 < 0.00001:
            data_10 = pyupbit.get_ohlcv(ticker=ticker10, interval="minute1")#(최대 200개까지 요청가능)
            # firstClose_10 = int(data_10.iloc[-2]['close'])# 종가
            firstVolume_10 = int(data_10.iloc[-2]['volume'])# 거래량
            # curClose_10 = int(data_10.iloc[-1]['close'])# 종가
            curVolume_10 = int(data_10.iloc[-1]['volume'])# 거래량
            time.sleep(0.2)

            if (firstVolume_10 * 2.0) < curVolume_10:
                macd1_10 = get_macd(ticker10, 12, 26, 9).iloc[-1]
                time.sleep(0.2)
                macd3_10 = get_macd(ticker10, 48, 104, 9).iloc[-1]
                time.sleep(0.2)
                if macd1_10 > 0 and macd3_10 < 0:
                    Envelopes2_10 = get_Envelopes(ticker10)
                    current_price_10 = get_current_price(ticker10)
                    time.sleep(0.2)
                    if Envelopes2_10 > current_price_10:
                        price_10 = pyupbit.get_current_price(ticker10)
                        time.sleep(0.2)
                        now_rsi_10 = rsi(data_10, 14).iloc[-1]
                        now_rsi2_10 = rsi(data_10, 14).iloc[-2]
                        time.sleep(0.2)
                        current_price_10 = get_current_price(ticker10)
                        time.sleep(0.2)
                        macd2_10 = get_macd(ticker10, 24, 52, 9).iloc[-1]
                        time.sleep(0.2)
                        Envelopes1_10 = get_Envelopes(ticker10) * 0.98
                        time.sleep(0.2)
                        # print("검색 10 완료")
                        ma20_10 = get_ma20(ticker10)
                        ma60_10 = get_ma60(ticker10)
                        ma120_10 = get_ma120(ticker10)
                        time.sleep(0.2)

# 매수
                        if krw > 5000 and get1_10 < 0.00001:
                            if macd1_10 > 0 and macd3_10 < 0 and current_price_10 < Envelopes1_10:

                                ret10 = upbit.buy_limit_order(ticker10, current_price_10, (krw * 0.9995) / current_price_10)
                                uuid10 = ret10['uuid']

                                price1_10 = price_10
                                del macd1_10, macd3_10, data_10, firstVolume_10, curVolume_10, now_rsi_10, now_rsi2_10, current_price_10, macd2_10, Envelopes1_10

                            if now_rsi_10 > now_rsi2_10 and macd1_10 > 0 and (macd1_10 > macd3_10 > macd2_10) and macd3_10 < 0 and (ma20_10 < ma60_10 or ma20_10 < ma120_10) and (ma20_10 > ma60_10 or ma20_10 > ma120_10) and current_price_10 > ma20_10:
                            # if now_rsi_10 > now_rsi2_10 and macd1_10 > 0 and (macd1_10 > macd3_10 > macd2_10) and macd3_10 < 0 and current_price_10 > ma20_10:

                                ret10 = upbit.buy_limit_order(ticker10, current_price_10, (krw * 0.9995) / current_price_10)
                                uuid10 = ret10['uuid']

                                price1_10 = price_10
                                del macd1_10, macd3_10, data_10, firstVolume_10, curVolume_10, now_rsi_10, now_rsi2_10, current_price_10, macd2_10, Envelopes1_10, ma20_10, ma60_10, ma120_10

                        if price1_10 > 1 and get1_10 < 0.00001:
                            if (price1_10 * 0.99) > price_10 or (price1_10 * 1.01) < price_10:

                                ret10 = upbit.cancel_order(uuid10)
                                del uuid10
    except:
        pass


# 매도
    try:
        won10 = pyupbit.get_current_price(ticker10)
        get2_10 = upbit.get_balance(ticker=ticker10)       
        time.sleep(0.2)
    except:
        pass
    try:
        if price1_10 > 1 and get2_10 > 0.00001:
            if won10 > (price1_10 * 1.007):
                ret10_10 = upbit.sell_limit_order(ticker10, won10, get2_10)
                uuid10_10 = ret10_10['uuid']
    except: 
        pass
    try:
        if price1_10 > 1 and get2_10 > 0.00001:
            if won10 < (price1_10 * 0.99):
                ret10_10 = upbit.cancel_order(uuid10_10)
    except: 
        pass
    try:
        if price1_10 > 1 and get2_10 > 0.00001:
            if won10 < (price1_10 * 0.99):
                upbit.sell_market_order(ticker10, get2_10)
                del uuid10_10, get2_10, price1_10, won10
    except: 
        pass