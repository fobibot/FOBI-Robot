# LSTM with Dropout for sequence classification in the IMDB dataset
import numpy as np
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
import pandas
from pythainlp.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
# fix random seed for reproducibility
np.random.seed(7)
# load the dataset but only keep the top n words, zero the rest

dataframe = pandas.read_csv("Datasets.csv", header=None)
dataset = dataframe.values

# temp = np.array(dataset)
# print(temp.shape)

X_train = [word_tokenize(x[0], engine='deepcut') for x in dataset] # now x_train is splited as word segmentation
Y_train = [x[1] for x in dataset]
# print(x_train)
temp = np.array(X_train) # (40, 1)
print(temp.shape)

encoder = LabelEncoder()
encoder.fit(Y_train)
encoded_Y = encoder.transform([x[1] for x in dataset])
dummy_y = np_utils.to_categorical(encoded_Y)
print(dummy_y)