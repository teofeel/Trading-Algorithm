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
    def __init__(self, symbol, price, data_earnings, open_position):
        self.symbol = symbol
        self.price = price
        self.data_stock_price = pd.DataFrame()
        self.data_earnings = data_earnings
        self.open_position = False
    
    def scrape_data(self):
        stock = pdr.get_data_yahoo(self.symbol,start = datetime(2010, 6, 29), end = datetime(2021,1,12))
        self.data_stock_price = pd.DataFrame(stock)
        self.data_stock_price.to_excel('D:\Code\Python\Trading Algorithm\ '+self.symbol+'.xlsx')
        #scrape data from yahoo finace

    def ema10(self):
        ema10 = self.data_stock_price
        ema10['EMA_10'] = self.data_stock_price['Close'].ewm(span = 10, adjust=False).mean()
        print (ema10.tail())  

    def ema50(self):
        ema50 = self.data_stock_price
        ema50['EMA_%0'] = self.data_stock_price['Close'].ewm(span = 50, adjust=False).mean()
        print (ema50.tail())  

    def ema200(self):
        ema200 = self.data_stock_price
        ema200['EMA_200'] = self.data_stock_price['Close'].ewm(span=200, adjust=False).mean()
        print (ema200.tail())  

    #def bollinger_bands(self)

    #def relative_strength_index(self)

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
        ema_9['Signal Line For MACD'] = self.data_stock_price['MACD'].ewm(span=9, adjust=False).mean()

        if self.data_stock_price['Signal Line For MACD'][self.data_stock_price.index[-1]] > self.data_stock_price['MACD'][self.data_stock_price.index[-1]]:
            return True
        elif self.data_stock_price['Signal Line For MACD'][self.data_stock_price.index[-1]] == self.data_stock_price['MACD'][self.data_stock_price.index[-1]]:
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


o1 = Option("tsla",0,0,False)
o1.scrape_data()
o1.MACD()