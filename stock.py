import pandas as pd
import pandas_datareader as pdr
import numpy as np
import backtrader as bt
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib

class Option:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price
        self.data_stock_price = pd.DataFrame()
        self.data_earnings = pd.DataFrame()
        self.open_position = False
    
    def scrape_data(self):
        stock = pdr.get_data_yahoo(self.symbol,start = datetime(2010, 6, 29), end = datetime.today())
        self.data_stock_price = pd.DataFrame(stock)
        self.data_stock_price.to_excel('D:\Code\Python\Trading Algorithm\ '+self.symbol+'.xlsx')
        #scrape data from yahoo finace

    def ema10(self):
        ema10 = self.data_stock_price
        ema10['EMA_10'] = self.data_stock_price['Close'].ewm(span = 10, adjust=False).mean()
        return self.data_stock_price['EMA_10'][self.data_stock_price.index[-1]]

    def ema50(self):
        ema50 = self.data_stock_price
        ema50['EMA_50'] = self.data_stock_price['Close'].ewm(span = 50, adjust=False).mean()
        return self.data_stock_price['EMA_50'][self.data_stock_price.index[-1]]

    def ema200(self):
        ema200 = self.data_stock_price
        ema200['EMA_200'] = self.data_stock_price['Close'].ewm(span=200, adjust=False).mean()
        return self.data_stock_price['EMA_200'][self.data_stock_price.index[-1]]  

    #def bollinger_bands(self)

    def relative_strength_index(self):
        def rsi(data, time_period):
            diff = data.diff().dropna() 

            up_change = 0*diff
            down_change = 0*diff

            up_change[diff>0]=diff[diff>0]
            down_change[diff<0]=diff[diff<0]

            avg_up = up_change.ewm(com = time_period-1, min_periods = time_period).mean()
            avg_down = down_change.ewm(com = time_period-1, min_periods = time_period).mean()

            rs = abs(avg_up/avg_down)
            rsi = 100 - 100/(1+rs)
            return rsi
            
        self.data_stock_price['RSI'] = rsi(self.data_stock_price['Adj Close'], 14)
        print(self.data_stock_price['RSI'][self.data_stock_price.index[-1]])
        

    #def momentum(self)

    #def volatility(self)

    def MACD(self):
        ema_12 = self.data_stock_price
        ema_26 = self.data_stock_price
        macd = self.data_stock_price
        ema_9 = self.data_stock_price
        
        ema_12['EMA_12'] = self.data_stock_price['Close'].ewm(span=12, adjust=False).mean()
        ema_26['EMA_26'] = self.data_stock_price['Close'].ewm(span=26, adjust=False).mean()
        macd['MACD'] = self.data_stock_price['EMA_12']-self.data_stock_price['EMA_26']
        ema_9['Signal Line'] = self.data_stock_price['MACD'].ewm(span=9, adjust=False).mean()

        if self.data_stock_price['Signal Line'][self.data_stock_price.index[-1]] > self.data_stock_price['MACD'][self.data_stock_price.index[-1]]:
            return True
        elif self.data_stock_price['Signal Line'][self.data_stock_price.index[-1]] == self.data_stock_price['MACD'][self.data_stock_price.index[-1]]:
            pass
        else:
            return False
        

    #def buy_order(self):
        #message via discord bot 
        #For example: Long {stock_name} at price: {price}

    #def sell_order(self):
        #message via discord bot 
        #For example: Short {stock_name} at price: {price}

    #def close_position(self):
        #message via discord bot 
        #For example: Close position of {stock_name} at price: {price}


o1 = Option("tsla",0)
o1.scrape_data()
o1.relative_strength_index()