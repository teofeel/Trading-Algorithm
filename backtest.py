import backtrader as bt
import pandas as pd 
import numpy as np
from datetime import datetime

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print ('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
    
    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.dataclose[0] < self.dataclose[-1]:
            if self.dataclose[-1] < self.dataclose[-2]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()


cerebro = bt.Cerebro()
cerebro.broker.set_cash(100000)

data = bt.feeds.YahooFinanceCSVData(
    dataname = 'TSLA.csv',
    fromdate = datetime(2000,1,1),
    todate = datetime(2020,12,31),
    reverse = False
)

cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)

print ('Strating Portfolio value %f' % cerebro.broker.getvalue())
cerebro.run()
print('Ending Portfolio value %f' % cerebro.broker.getvalue())