import pandas as pd 
import pandas.io as web
import numpy as np



stocks = []

'''
if ((stock.MACD() and stock.price > stock.ema200()) or (stock.bollinger_band()<0 and stock.relative_strength_index()) or (stock.momentum()>-0.2 and stock.volatility()>=1.5 and stock.MACD()>0)) 
        buy stock
'''

stocks_for_trading = []
options = []
etf = []
futures = []


