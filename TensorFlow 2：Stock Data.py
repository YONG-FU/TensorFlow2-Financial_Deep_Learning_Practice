import pandas_datareader as pdr
import datetime
import matplotlib.pyplot as plt

start = datetime.datetime(2014, 1, 1)
end = datetime.date.today()

stock = 'TSLA'
data = pdr.DataReader(stock, 'yahoo', start, end)

import pandas as pd

indicators = pd.DataFrame(index=data.index)
# 50 day
short_window = 50
# 200 day
long_window = 200
# Exponential moving averages using the closing data
indicators['short_avg'] = data['Close'].ewm(span=short_window, adjust=False).mean()
indicators['long_avg'] = data['Close'].ewm(span=long_window, adjust=False).mean()

indicators.plot()
data.plot()
plt.show()

# Getting the S&P 500 relative price difference.
SP = pdr.DataReader('SPY', 'yahoo', start, end)
SP['sp_percent_change'] = SP['Adj Close'].pct_change(periods=1).astype(float)
data = data.merge(SP['sp_percent_change'], left_index=True, right_index=True)
data['percent_change'] = data['Adj Close'].pct_change(periods=1).astype(float)
# Daily percent change as compared to the S&P 500
data['relative_change'] = data['percent_change'] - data['sp_percent_change']

from finta import TA
indicators = {'SMA', 'SMM', 'SSMA', 'EMA', 'DEMA', 'TEMA', 'TRIMA', 'TRIX', 'VAMA', 'ER', 'KAMA', 'ZLEMA', 'WMA', 'HMA'}

df = None

# Using python's eval function to create a method from a string instead of having every method define
for indicator in indicators:
    df = eval('TA.' + indicator + '(data)')
    if not isinstance(df, pd.DataFrame):
        df = df.to_frame()
    df = df.add_prefix(indicator + '_')
    data = data.merge(df, left_index=True, right_index=True)

data = data.fillna(data.mean())
print(data.describe())

import numpy as np
for column in data:
    print(type(column))
    data[column] = np.log(data[column])

close = data['Close']
print(close.describe())

close.plot(label='Close')
EMA = data['EMA_9 period EMA']
EMA.plot(label='EMA')

plt.title('Exponential Moving Averages of Close Prices by Date')
plt.legend()

data.to_csv("Stock Data Analysis.csv")
plt.show()