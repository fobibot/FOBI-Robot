from pythainlp.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import OneHotEncoder
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
# from keras.utils import *
from sklearn.model_selection import train_test_split
import numpy as np
import pandas
import os


class MachineLearning:
    def __init__(self):
        self.dataset = None
        self.input_dataset = []
        self.output_dataset = []
        self.flat_set_of_input_list
        self.flat_set_of_output
        self.number_of_category
        self.max_word_lenght = 30
        self.encoded_train_x_datasets
        self.encoded_train_y_datasets
        self.model

        self.encoder_input = LabelEncoder()
        self.encoder_output = LabelEncoder()

        self.LoadDatasets("Datasets.csv")
        self.PreProcessDatasets()
        self.CreateInputLabelEncoder()
        self.CreateOutputLabelEncoder()
        self.TransformInputDatasets2EncodeValue()
        self.TransformOutputDatasets2EncodeValue()
        self.X_train, self.X_test, self.y_train, self.y_test = self.TrainTestSplit()
        self.ModelStructure()
        self.CreateModel()

    def LoadDatasets(self, _dir):
        dataframe = pandas.read_csv(_dir, header=None)
        self.dataset = dataframe.values

    def PreProcessDatasets(self):
        # input_dataset = []
        # output_dataset = []
        for data in self.dataset:
            self.input_dataset.append(word_tokenize(data[0], engine='deepcut'))
            self.output_dataset.append(data[1])
        print(self.input_dataset)
        flat_input_list = [
            item for sublist in self.input_dataset for item in sublist]
        self.flat_set_of_input_list = list(set(flat_input_list))
        self.flat_set_of_output = list(set(self.output_dataset))
        # print("Flat set of Input Datasets",flat_set_of_input_list)
        # print("Output dataset", flat_set_of_output)

    def CreateInputLabelEncoder(self):
        # Encode All of input datasets words from string to number
        # self.encoder_input = LabelEncoder()
        self.encoder_input.fit(self.flat_set_of_input_list)
        np.save("Model/Encoded_Input_classes.npy",
                self.encoder_input.classes_)  # Save Encoded Model
        print("Encoder Input Classes :", self.encoder_input.classes_)

    def CreateOutputLabelEncoder(self):
        # Encode All of output datasets words from string to number
        self.encoder_output.fit(self.flat_set_of_output)
        np.save("Model/Encoded_Output_classes.npy",
                self.encoder_output.classes_)  # Save Encoded Model

        self.number_of_category = len(self.encoder_output.classes_)
        print("Encoder Output has", self.number_of_category,
              "Classes :", self.encoder_output.classes_)

    def TransformInputDatasets2EncodeValue(self):
        self.encoded_train_x_datasets = sequence.pad_sequences([list(self.encoder_input.transform(
            sentence)) for sentence in self.input_dataset], maxlen=self.max_word_lenght)
        print("Encoded Train_X dataset has", len(
            self.encoded_train_x_datasets), ":\n", self.encoded_train_x_datasets)

    def TransformOutputDatasets2EncodeValue(self):
        self.encoded_train_y_datasets = np_utils.to_categorical(
            self.encoder_output.transform(self.output_dataset))
        print("Encoded Train_Y dataset :\n", self.encoded_train_y_datasets)

    def TrainTestSplit(self, test_size=0.33):
        seed = 7
        np.random.seed(seed)
        X_train, X_test, y_train, y_test = train_test_split(
            self.encoded_train_x_datasets, self.encoded_train_y_datasets, test_size=test_size, random_state=seed)
        return X_train, X_test, y_train, y_test

    def ModelStructure(self):
        self.model = Sequential()
        self.model.add(Embedding(self.max_word_lenght, self.max_word_lenght))
        self.model.add(LSTM(self.max_word_lenght, dropout=0.2, recurrent_dropout=0.1))
        self.model.add(Dense(self.max_word_lenght, activation='relu'))
        self.model.add(Dense(self.max_word_lenght, activation='sigmoid'))
        self.model.add(Dense(self.max_word_lenght, activation='sigmoid'))
        self.model.add(Dense(self.number_of_category, activation='sigmoid'))

        self.model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

    def CreateModel(self):
        self.model.fit(self.X_train, self.y_train, validation_data=(self.X_test, self.y_test),
                  batch_size=32,
                  epochs=300)
        self.model.save('model.h5')


    def Predict(self, input):
        # predictions = self.model.predict(input)
        # pre = []
        # for x in predictions:
        #     pre.append(x.tolist().index(max(x)))
        # # round predictions
        # rounded = [round(x[0]) for x in predictions]
        # print(predictions, pre)
        return self.model.predict(input)
    
