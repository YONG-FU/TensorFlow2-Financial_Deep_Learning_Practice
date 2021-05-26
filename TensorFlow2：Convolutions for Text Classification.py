import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing import text, sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Conv1D, GlobalMaxPool1D, MaxPooling1D
from sklearn.model_selection import train_test_split

print(tf.__version__)

# Load Data
train_df = pd.read_csv('train.csv').fillna(' ')
train_df.sample(10, random_state=1)

x = train_df['comment_text'].values
print(x)

# View few toxic comments
train_df.loc[train_df['toxic'] == 1].sample(10, random_state=10)

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

comments = train_df['comment_text'].loc[train_df['toxic'] == 1].values
wordcloud = WordCloud(
    width=640,
    height=640,
    background_color='black',
    stopwords=STOPWORDS).generate(str(comments))
fig = plt.figure(
    figsize=(12, 8),
    facecolor='k',
    edgecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

y = train_df['toxic'].values
print(y)

# Plot frequency of toxic comments
train_df['toxic'].plot(kind='hist', title='Distribution of Toxic Comments')
plt.show()

train_df['toxic'].value_counts()

# Data Preparation - Tokenize and Pad Text Data
max_features = 20000
max_text_length = 400

x_tokenizer = text.Tokenizer(max_features)
x_tokenizer.fit_on_texts(list(x))
x_tokenized = x_tokenizer.texts_to_sequences(x)
x_train_val = sequence.pad_sequences(x_tokenized, maxlen=max_text_length)

# Prepare Embedding Matrix with Pre-trained GloVe Embeddings
embedding_dim = 100
embedding_index = dict()
f = open('glove.6B.100d.txt')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embedding_index[word] = coefs
f.close()
print(f'Found {len(embedding_index)} word vectors.')

embedding_matrix = np.zeros((max_features, embedding_dim))
for word, index in x_tokenizer.word_index.items():
    if index > max_features - 1:
        break
    else:
        embedding_vector = embedding_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[index] = embedding_vector

# Create the Embedding Layer
model = Sequential()
model.add(Embedding(max_features,
                    embedding_dim,
                    embeddings_initializer=tf.keras.initializers.Constant(embedding_matrix),
                    trainable=False))
model.add(Dropout(0.2))

# Build the Model
filters = 250
kernel_size = 3
hidden_dims = 250
model.add(Conv1D(filters,
                 kernel_size,
                 padding='valid'))
model.add(MaxPooling1D())
model.add(Conv1D(filters,
                 5,
                 padding='valid',
                 activation='relu'))
model.add(GlobalMaxPool1D())
model.add(Dense(hidden_dims, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(1, activation='sigmoid'))
model.summary()

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train Model
x_train, x_val, y_train, y_val = train_test_split(x_train_val, y,
                                                  test_size=0.15, random_state=1)
batch_size = 32
epochs = 3

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=3,
          validation_data=(x_val, y_val))

# Evaluate Model
test_df = pd.read_csv('test.csv')
x_test = test_df['comment_text'].values

x_test_tokenized = x_tokenizer.texts_to_sequences(x_test)
x_testing = sequence.pad_sequences(x_test_tokenized, maxlen=max_text_length)

y_testing = model.predict(x_testing, verbose=1, batch_size=32)
y_testing.shape
y_testing[0]

test_df['Toxic'] = ['not toxic' if x < .5 else 'toxic' for x in y_testing]
test_df[['comment_text', 'Toxic']].head(20)
