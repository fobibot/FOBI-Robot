from __future__ import print_function

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.datasets import imdb
import pandas
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils

import numpy as np
import math
from keras.models import load_model
import function as fn

import numpy as np
import time as t
from pythainlp.tokenize import word_tokenize

dataframe = pandas.read_csv("Datasets.csv", header=None)
dataset = dataframe.values


label_encoder = LabelEncoder()
# label_encoder.fit([x[1] for x in dataset] )
label_encoder.classes_ = np.load('Model/Encoded_Output_classes.npy')
label_encoded = label_encoder.transform([x[1] for x in dataset])
dummy_y = np_utils.to_categorical(label_encoded)
print(list(label_encoder.classes_))

data_encoder = LabelEncoder()
data_encoder.classes_ = np.load('Model/Encoded_Input_classes.npy')
print(list(data_encoder.classes_))

model = load_model('Model/model.h5')
while True:
	inp = input('Input:')
	last = t.time()
	data_encoder = LabelEncoder()
	data_encoded = fn.DataEncoder(data_encoder, dataset, [inp])
	print(data_encoded)


	x_test = sequence.pad_sequences(data_encoded, maxlen=10)
	now = t.time()
	print("Encode data used", now-last, "sec")

	last = t.time()
	predictions = model.predict(x_test)
	now = t.time()
	print("Predict data used", now-last, "sec")
	pre = []
	for x in predictions:
	    pre.append(x.tolist().index(max(x)))
	# round predictions
	rounded = [round(x[0]) for x in predictions]
	print(pre)
	print(label_encoder.inverse_transform(pre))
