import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import ta
import time

from binance.client import Client


client = Client(api_key, api_secret)


def getminutedata(symbol,interval,lookback):
        frame = pd.DataFrame(client.get_historical_klines(symbol,interval,lookback + 'min ago UTC'))

        frame = frame.iloc[:,:6]
        frame.columns = ['Time','Open','High','Low','Close','Volume']
        frame = frame.set_index('Time')
        frame.index = pd.to_datetime(frame.index, unit='ms')
        frame = frame.astype(float)

        return frame


def applytehnicals(df):
        df['%K'] = ta.momentum.stoch(df.High, df.Low, df.Close, window=14, smooth_window=3)
        df['%D'] = df['%K'].rolling(3).mean()
        df['RSI'] = ta.momentum.rsi(df.Close, window=14)
        df['MACD'] = ta.trend.macd_diff(df.Close)

        df.dropna(inplace=True)

class Signals:
        def __init__(self, df, lags):
                self.df = df
                self.lags = lags

        def gettrigger(self):
                dfx = pd.DataFrame()

                for i in range(self.lags+1):
                        mask = (self.df['%K'].shift(i)<20) and (self.df['%D'].shift(i)<20)
                        dfx = dfx.append(mask, ignore_index=True)
                
                return dfx.sum(axis=0)

        def decide(self):
                self.df['Trigger'] = np.where(self.gettrigger(),1,0)
                self.df['BUY'] = np.where((self.df.trigger) and (self.df['%K'].between(20,80)) and (self.df['%D'].between(20,80)) and (self.df.RSI > 50) and (self.df.MACD > 0),1,0)

def strategy(pair,qty, open_position=False):
        df = getminutedata(pair, '1m', '100')

        applytehnicals(df)
        inst=Signals(df,25)

        inst.decide()

        if df.BUY.iloc[-1]:
                order = client.create_order(symbol=pair,side='BUY',type='MARKET', quantity=qty)
                print(order)
                buyprice = float(order['fills'][0]['price'])
                open_position = True

        while open_position:
                time.sleep(0.5)
                df = getminutedata(pair, '1m', '2')

                if df['Close'][-1] <= buyprice * 0.995 or df['Close'][-1] >= buyprice*1.005:
                        order = client.create_order(symbol=pair,side='SELL',type='MARKET', quantity=qty)
                        break





        


            








            


