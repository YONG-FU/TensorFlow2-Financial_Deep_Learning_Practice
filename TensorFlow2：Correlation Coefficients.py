import pandas_datareader as pdr
import datetime
import matplotlib.pyplot as plt

start = datetime.datetime(2014, 1, 1)
end = datetime.date.today()

stock = 'GOOGL'
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

df = None

stock = 'TSLA'
df = pdr.DataReader(stock, 'yahoo', start, end)

print(df['Close'][0])

from finta import TA

# Here are all indicators we are using
stocks_to_compare = ['TSLA', 'GOOGL']

# Using python eval function to create a method from a string instead of having every method defined
# Merge data frames based on the date
data = data.merge(df, left_index=True, right_index=True)

data = data.fillna(data.mean())

import numpy as np

for column in data:
    print(type(column))
    data[column] = np.log(data[column])

close = data['Close_y']
print(close.describe())

print(close[0])
close.plot(label="Close_y")
close2 = data['Close_x']
close2.plot(label='Close_x')

plt.title('Exponential Moving Averages of Close Prices by Date')
plt.legend()

data.to_csv('CSV：Stock Data Analysis.csv')

compare_data = close.to_frame().merge(close2.to_frame(), left_index=True, right_index=True)

import seaborn as sns

sns.pairplot(compare_data, vars=["Close_x", "Close_y"], dropna=True)

from scipy.stats.stats import pearsonr

rets = compare_data.pct_change()

print(data.describe())

corr = rets.corr(method='pearson')
corr.to_csv('CSV：Correlations Analysis.csv')

plt.figure(figsize=(10, 6))
plt.scatter(rets.mean(), rets.std())
plt.xlabel('Expected returns')
plt.ylabel('Risk')

for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
    plt.annotate(label, xy=(x, y), xytext=(20, -20), textcoords='offset points',
                 ha='right', va='bottom', arrowprops=dict(connectionstyle='arc3, rad=0'))
    plt.title('Scatter plot of Risk and Returns')

df.plot()
data.plot()
plt.show()
