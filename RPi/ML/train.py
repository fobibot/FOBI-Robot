from pythainlp.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
# from keras.utils import *
import numpy as np
import pandas
import os
import numpy as np
from numpy import ndarray

dataframe = pandas.read_csv("Datasets.csv", header=None)
dataset = dataframe.values


encoder = LabelEncoder()
encoder.fit([x[1] for x in dataset] )
encoded_Y = encoder.transform([x[1] for x in dataset] )
dummy_y = np_utils.to_categorical(encoded_Y)
np.save('Encoded_Output_classes.npy', encoder.classes_)

print(dummy_y)

bar = [word_tokenize(x[0],engine='deepcut') for x in dataset ]
bar_dimension = [len(x) for x in bar]
encoder2 = LabelEncoder()
encoder2.fit([j for i in bar for j in i])
encoded_Y2 = encoder2.transform([j for i in bar for j in i] )
print("y2")
print(encoded_Y2)
np.save('Encoded_Input_classes.npy', encoder2.classes_) # save Encoded Input Model

text_data = []


for x in range(len(bar)):
    temp_data = []
    for i in range(bar_dimension[x]):
        temp_data.append(encoded_Y2[0])
        encoded_Y2 = np.delete(encoded_Y2,0)
    text_data.append(temp_data)

max_word_lenght = 80
x_train = sequence.pad_sequences(text_data, maxlen=max_word_lenght)
print(x_train)
print(text_data)
print(dummy_y)


model = Sequential()
model.add(Embedding(max_word_lenght, max_word_lenght))
model.add(LSTM(max_word_lenght, dropout=0.1, recurrent_dropout=0.1))
# model.add(Dense(max_word_lenght, activation='relu'))
# model.add(Dense(max_word_lenght, activation='sigmoid'))
# model.add(Dense(max_word_lenght, activation='sigmoid'))
model.add(Dense(4, activation='sigmoid'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print(len(x_train))
model.fit(x_train, dummy_y,
          batch_size=32,
          epochs=100)


predictions = model.predict(x_train)
pre = []
for x in predictions:
    pre.append(x.tolist().index(max(x)))
# round predictions
rounded = [round(x[0]) for x in predictions]
print(predictions,pre)
model.save('model.h5')

