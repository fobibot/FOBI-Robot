from pythainlp.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from sklearn.model_selection import train_test_split
import numpy as np
import pandas
import os
import json

# Load Datasets
dataframe = pandas.read_csv("New_ML/Datasets_G_NewLabel.csv", header=None)
dataset = dataframe.values

def LoadJsonFile(filename):
    try:
        with open(filename) as json_data:
            json_file = json.load(json_data)
    except:
        print("No file name", filename, ".json")
        pass
    return json_file

remove_words = LoadJsonFile("New_ML/MustRemoveWord.json")
print(remove_words)

# Seperate Dataset into input and output datasets
input_dataset = []
output_dataset = []
for data in dataset: # remove frequence words
    sentence = word_tokenize(data[0], engine='deepcut')
    for word in sentence:
        if word in remove_words:
            sentence.remove(word)
    input_dataset.append(sentence)
    output_dataset.append(data[1])
print(input_dataset)

flat_input_list = [item for sublist in input_dataset for item in sublist] # Convert list of list to list
flat_set_of_input_list = list(set(flat_input_list))
flat_set_of_output = list(set(output_dataset))
print("Flat set of Input Datasets",flat_set_of_input_list)
print("Output dataset", flat_set_of_output)

# Encode All of input datasets words from string to number
encoder_input = LabelEncoder()
encoder_input.fit(flat_set_of_input_list)
np.save("New_ML/Saved_Model/Encoded_Input_classes.npy" , encoder_input.classes_) # Save Encoded Model
print("Encoder Input Classes :",encoder_input.classes_)

# Encode All of output datasets words from string to number
encoder_output = LabelEncoder()
encoder_output.fit(flat_set_of_output)
np.save("New_ML/Saved_Model/Encoded_Output_classes.npy" , encoder_output.classes_) # Save Encoded Model

number_of_category = len(encoder_output.classes_)
print("Encoder Output has", number_of_category, "Classes :",encoder_output.classes_)

# transform input data to encoded
max_word_lenght = 30
encoded_train_x_datasets = sequence.pad_sequences( [list(encoder_input.transform(sentence)) for sentence in input_dataset], maxlen=max_word_lenght )
print("Encoded Train_X dataset has",len(encoded_train_x_datasets), ":\n", encoded_train_x_datasets)

# transform output data to encoded
encoded_train_y_datasets = np_utils.to_categorical( encoder_output.transform(output_dataset) )
print("Encoded Train_Y dataset :\n", encoded_train_y_datasets)

# Train Test Split
seed = 7
np.random.seed(seed)
X_train, X_test, y_train, y_test = train_test_split(encoded_train_x_datasets, encoded_train_y_datasets, test_size=0.2, random_state=seed)

# ML Model Structure
max_features = 2000
model = Sequential()
model.add(Embedding(max_features, max_word_lenght))
model.add(LSTM(max_word_lenght, dropout=0.1, recurrent_dropout=0.1))
model.add(Dense(max_word_lenght, activation='sigmoid'))
model.add(Dense(number_of_category, activation='softmax')) #softmax used for highlight the largest values and suppress values which are significantly below the maximum value

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X_train, y_train, validation_data=(X_test,y_test),
          batch_size=32,
          epochs=100)

predictions = model.predict(X_test)
pre = []
for x in predictions:
    pre.append(x.tolist().index(max(x)))
# round predictions
rounded = [round(x[0]) for x in predictions]
print(predictions,pre)
model.save('New_ML/Saved_Model/model.h5')