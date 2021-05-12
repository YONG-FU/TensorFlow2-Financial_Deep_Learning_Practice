# import pandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

import matplotlib.style
import matplotlib as mpl

mpl.style.use('ggplot')

from matplotlib.pylab import rcParams

rcParams['figure.figsize'] = 20, 10

from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import MaxAbsScaler

scaler = MinMaxScaler(feature_range=(-1, 1))
##scaler = MaxAbsScaler()
##scaler = StandardScaler()
##scaler = Normalizer()
##scaler = QuantileTransformer(output_distribution='normal',copy=False)
##scaler = RobustScaler()
##scaler = PowerTransformer()

from tensorflow.keras.mixed_precision import experimental as mixed_precision
import tensorflow as tf
from tensorflow.keras import layers

new_policy = mixed_precision.Policy('float64')


# get data
def GetData(fileName):
    return pd.read_csv(fileName, header=0, parse_dates=[0])


# read time series from the exchange.csv file
exchangeRatesSeries = GetData('exercise_data/GBPUSD_D1.csv')

lr_data = pd.DataFrame(exchangeRatesSeries, index=range(0, len(exchangeRatesSeries)))

# We'll create a separate dataset so that new features don't mess up the original data.
##print("Copying from CSV and dropping columns ",lr_data.columns)
##lr_data = exchangeRatesSeries.drop(columns=['Open','High','Low'], inplace=True)
print("Finished copying from CSV and dropping columns", lr_data.columns)

print("Date conversion")
lr_data['Date'] = pd.to_datetime(lr_data.Date, format='%Y-%m-%d')
print("Date conversion complete")

print("Sorting by date")
lr_data = lr_data.sort_values(by='Date')
print("Finished sorting")

##new_data = pd.DataFrame(index=range(0, len(lr_data)), columns=['Date', 'GBP/USD Close'])
##
##for i in range(0,len(exchangeRatesSeries)):
##    new_data['Date'][i] = lr_data['Date'][i]
##    new_data['GBP/USD Close'][i] = lr_data['GBP/USD Close'][i]
##

print(lr_data['Date'].dtype)
length = len(lr_data['Date'])


def iterate_it(frame):
    print('mem: ', frame.memory_usage())
    for index, row in frame.iterrows():
        frame['Date'].replace({frame['Date'][index]: frame['Date'][index].toordinal()}, inplace=True)
        if (int(index) == (int(length / 100))):
            print("1%")
        if (int(index) == (int(length / 10))):
            print("10%")
        if (int(index) == (int(length / 2))):
            print("Halfway there")
    return frame['Date']


date_store = lr_data['Date'].to_frame()
print('Replacing with ordinals, len= ', length)

##for t in lr_data.itertuples():
##    lr_data['Date'].replace({lr_data['Date'][t]: lr_data['Date'][t].toordinal()}, inplace=True)
lr_data['Date'] = iterate_it(lr_data)
print('Finished replacing with ordinals')

##lr_data = lr_data.sort_values(by='Date')
lr_data = pd.DataFrame(lr_data, index=range(0, len(exchangeRatesSeries)))

lr_data.drop(columns=['Volume'], inplace=True)

lr_data_temp = np.asarray(tf.reshape(lr_data['GBP/USD Close'], (len(lr_data), 1)))

print(lr_data_temp)
print(type(lr_data_temp))
print(len(lr_data_temp))
print(len(lr_data['GBP/USD Close']))

lr_data['GBP/USD Close'] = scaler.fit_transform(lr_data_temp)
print(lr_data.squeeze)
##new_data = pd.DataFrame(new_data,index=range(0, len(lr_data)), columns=['Date', 'GBP/USD Close'])

##for t in new_data['Date']:
##    t = pd.to_datetime(t)
##    new_data['Date'].replace({t: t.toordinal()}, inplace=True)
ans = lr_data.to_numpy()
print()
# Train-test split
##for i in range(0,len(lr_data)):
##    ans[i] = lr_data.iloc[[i]]
print(type(ans[0]))
ans2 = [y for x, y in date_store.groupby('Date', as_index=False)]

print('ans', ans[1])

slice_size = int(length * .75)
print(slice_size)
train = ans[:slice_size]
print(len(train))
print(len(ans))

print(train[0])
date_store_first = ans2[:slice_size]

print(float(train[0][0]))

train1 = pd.DataFrame(train, index=range(0, len(train)), columns=('Date', 'Open', 'High', 'Low', 'GBP/USD Close'),
                      dtype='float64')
print(train1)
print(train1.columns)

####for i in range(0,len(train)):
##for index, row in train1.iterrows():
##        train1['Date'].replace({train1['Date']: train[index][0]}, inplace=True)
##        train1['Open'].replace({train1['Open'][index]: train[index][1]}, inplace=True)
##        train1['High'].replace({train1['High'][index]: train[index][2]}, inplace=True)
##        train1['Low'].replace({train1['Low'][index]: train1[index][3]}, inplace=True)
##        train1['GBP/USD Close'].replace({train1['GBP/USD Close'][index]: train1[index][4]}, inplace=True)
##        train1['Volume'].replace({train1['Volume'][index]: train1[index][5]}, inplace=True)
##print(train1)

##train1=train1.transpose()
test = ans[slice_size:]
print('fixed datestore? ', date_store_first[0].Date)
print('fixed datestore type? ', type(date_store_first))

date_store_second = ans2[slice_size:]

test1 = pd.DataFrame(test, index=range(0, len(test)), columns=('Date', 'Open', 'High', 'Low', 'GBP/USD Close'))
##for i in range(0,len(test)):
##    test1.replace(['Date'][i] , float(test[i][0]))
##    test1.replace(['Open'][i] , float(test[i][1]))
##    test1.replace(['High'][i] , float(test[i][2]))
##    test1.replace(['Low'][i] , float(test[i][3]))
##    test1.replace(['GBP/USD Close'][i] ,float(test[i][4]))
##    test1.replace(['Volume'][i] , float(test[i][5]))

##test1=test1.transpose()


from sklearn.model_selection import train_test_split

x_train = pd.DataFrame(train1, index=range(0, len(train)), columns=('Date', 'Open', 'High', 'Low', 'GBP/USD Close'))
y_train = pd.DataFrame(train1, index=range(0, len(train)), columns=(['GBP/USD Close']))

print(x_train.columns)
print(y_train.columns)

##y_train = train1['GBP/USD Close'].to_frame()
##x_train = train1.drop(['GBP/USD Close'])

x_test = pd.DataFrame(test1, index=range(0, len(test)), columns=('Date', 'Open', 'High', 'Low', 'GBP/USD Close'))
y_test = pd.DataFrame(test1, index=range(0, len(test)), columns=(['GBP/USD Close']))
##y_test = test1['GBP/USD Close'].to_frame()
##x_test = test1.drop(['GBP/USD Close'])
print('xtest len: ', len(x_test))
print(x_train)
print(y_train)

##np.polynomial.polynomial.Polynomial.fit(np.array(x_train.to_numpy().ravel()).astype('float64'),np.array(y_train.to_numpy().ravel()).astype('float64'),1)


# Implementing linear regression
from sklearn.linear_model import LinearRegression
from sklearn import neighbors
from sklearn.model_selection import GridSearchCV

##model = LinearRegression(fit_intercept=True, normalize=False, n_jobs=-1)
##params = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}
##knn = neighbors.KNeighborsRegressor()
##model = GridSearchCV(knn, params, cv=5)


model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Dense(512, activation='linear'))

model.add(tf.keras.layers.Dense(256, activation='linear'))

model.add(tf.keras.layers.Dense(128, activation='linear'))

model.add(tf.keras.layers.Dense(32, activation='linear'))

model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(optimizer=tf.optimizers.Nadam(), loss='mean_squared_error')

with tf.device('/GPU:0'):
    x_tf_train = tf.convert_to_tensor(x_train.astype('float64'))
    print(x_tf_train.shape)
    y_tf_train = tf.convert_to_tensor(y_train.astype('float64'))
    print(y_tf_train.shape)

    model.fit(x_tf_train, y_tf_train, epochs=100)

    x_tf_test = tf.convert_to_tensor(x_test.astype('float64'))
    y_tf_test = tf.convert_to_tensor(y_test.astype('float64'))

    preds = model.predict(x_tf_test)
    ##rmse = np.sqrt(metrics.mean_squared_error(y_test, preds))

m = tf.keras.metrics.RootMeanSquaredError()
print(type(m))
m.update_state(y_tf_test, preds)
print(type(m))

m = m.result().numpy()
print(type(m))

rmse = m
print(rmse)
print('pred_length ', len(preds))

preds = scaler.inverse_transform(preds)

temp = pd.DataFrame(index=range(0, len(preds)), columns=('Date', 'Predictions'))
for i in range(0, len(preds)):
    temp['Date'][i] = test1['Date'][i]
    temp['Predictions'][i] = float(preds[i])

print(preds)
print(preds.shape)
preds = pd.DataFrame(index=range(0, len(preds)))

preds = temp

print(preds)
print(preds.shape)
print(type(date_store_first[1]['Date'].values[0]))

test1['Predictions'] = 0

test1['Predictions'] = preds['Predictions']
##print(date_store_first[1])
date_temp1 = pd.DataFrame(index=range(0, len(date_store_first)), columns=(['Date']))
for i in range(0, len(date_temp1)):
    date_temp1['Date'][i] = date_store_first[i].Date.values[0]
##    date_temp1['Date'].apply(pd.to_datetime(date_temp1['Date'][i], format='%Y-%m-%d'))
date_temp2 = pd.DataFrame(index=range(0, len(date_store_second)), columns=(['Date']))
for i in range(0, len(date_temp2)):
    date_temp2['Date'][i] = date_store_second[i].Date.values[0]

##date_store_first = pd.DataFrame(date_temp1.values,index=range(0, len(date_store_first)),columns=(['Date']))
##date_store_second = pd.DataFrame(date_temp2,index=range(0, len(date_store_second)),columns=(['Date']))
print(type(date_temp1.Date))
date_temp1['Date'] = pd.to_datetime(date_temp1.Date.values, format='%Y-%m-%d')
date_temp2['Date'] = pd.to_datetime(date_temp2.Date.values, format='%Y-%m-%d')

train1['Date'] = date_temp1
print(train1['GBP/USD Close'].shape)
print(train1['GBP/USD Close'].shape)

train1['GBP/USD Close'] = scaler.inverse_transform(train1['GBP/USD Close'].values.reshape(-1, 1))

test1['Date'] = date_temp2
test1['GBP/USD Close'] = scaler.inverse_transform(test1['GBP/USD Close'].values.reshape(-1, 1))

print(test1)

print(preds)
plt.plot(train1['Date'], train1['GBP/USD Close'])
plt.plot(test1['Date'], test1[['Predictions', 'GBP/USD Close']])
plt.xlabel('Date')
plt.ylabel('Close')

plt.xlim(train1.Date.min(), test1.Date.max())
plt.ylim(train1['GBP/USD Close'].min(), train1['GBP/USD Close'].max())

plt.title('compare')

##print(model.score(x_test,y_test))

plt.show()
