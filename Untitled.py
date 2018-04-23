
# coding: utf-8

# In[61]:


from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
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
import numpy
import json
import pandas


# In[62]:


def LoadJsonFile(filename):
    try:
        with open(filename) as json_data:
            json_file = json.load(json_data)
    except (UnboundLocalError, FileNotFoundError):
        print("No file name", filename, ".json")
        pass
    return json_file

remove_words = LoadJsonFile("MustRemoveWord.json")
print(remove_words)


# In[63]:


# Load Datasets
dataframe = pandas.read_csv("Datasets_G_NewLabel.csv", header=None)
dataset = dataframe.values

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
np.save("Saved_Model/Encoded_Input_classes.npy" , encoder_input.classes_) # Save Encoded Model
print("Encoder Input Classes :",encoder_input.classes_)

# Encode All of output datasets words from string to number
encoder_output = LabelEncoder()
encoder_output.fit(flat_set_of_output)
np.save("Saved_Model/Encoded_Output_classes.npy" , encoder_output.classes_) # Save Encoded Model

number_of_category = len(encoder_output.classes_)
print("Encoder Output has", number_of_category, "Classes :",encoder_output.classes_)

# transform input data to encoded
max_word_lenght = 30
encoded_train_x_datasets = sequence.pad_sequences( [list(encoder_input.transform(sentence)) for sentence in input_dataset], maxlen=max_word_lenght )
print("Encoded Train_X dataset has",len(encoded_train_x_datasets), ":\n", encoded_train_x_datasets)

# transform output data to encoded
encoded_train_y_datasets = np_utils.to_categorical( encoder_output.transform(output_dataset) )
print("Encoded Train_Y dataset :\n", encoded_train_y_datasets)


# In[64]:


from sklearn.metrics import r2_score

def performance_metric(y_true, y_predict):
    """ Calculates and returns the performance score between 
        true and predicted values based on the metric chosen. """
    
    # TODO: Calculate the performance score between 'y_true' and 'y_predict'
    score = r2_score(y_true, y_predict)
    
    # Return the score
    return score


# In[65]:


# TODO: Import 'train_test_split'

from sklearn.model_selection import train_test_split

# TODO: Shuffle and split the data into training and testing subsets
X_train, X_test, y_train, y_test = train_test_split(encoded_train_x_datasets, encoded_train_y_datasets, test_size=0.2, random_state=42)

# Success
print("Training and testing split was successful.")


# In[97]:


from sklearn.metrics import make_scorer
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import ShuffleSplit
import numpy as np

def fit_model(X, y, model):
    """ Performs grid search over the 'max_depth' parameter for a 
        decision tree regressor trained on the input data [X, y]. """
    
    # Create cross-validation sets from the training data
    # sklearn version 0.18: ShuffleSplit(n_splits=10, test_size=0.1, train_size=None, random_state=None)
    # sklearn versiin 0.17: ShuffleSplit(n, n_iter=10, test_size=0.1, train_size=None, random_state=None)
    cv_sets = ShuffleSplit(X.shape[0], n_iter = 10, test_size = 0.20, random_state = 0)


    # TODO: Create a dictionary for the parameter 'max_depth' with a range from 1 to 10
    # params = {'epochs ':np.arange(50,300,50), 'batch_size':np.arange(10,50,5)}
    # params = dict(epochs=np.arange(20,180,25), loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=['adam', 'Nadam', 'Adamax', 'Adadelta', 'RMSprop'])
    params = {'optimizers':['adam', 'Nadam', 'Adamax', 'Adadelta', 'RMSprop'], 
              'epochs':np.arange(20,180,25),
              'losses':['categorical_crossentropy', 'mean_squared_error']}

    # TODO: Create the grid search cv object --> GridSearchCV()
    # Make sure to include the right parameters in the object:
    # (estimator, param_grid, scoring, cv) which have values 'regressor', 'params', 'scoring_fnc', and 'cv_sets' respectively.
    grid = GridSearchCV(estimator=model, param_grid=params, cv=cv_sets)

    # Fit the grid search object to the data to compute the optimal model
    grid = grid.fit(X, y)

    # Return the optimal model after fitting the data
    return grid.best_estimator_


# In[95]:


def create_model(losses='categorical_crossentropy', optimizers='adam'):
    max_features = 2000
    model = Sequential()
    model.add(Embedding(max_features, max_word_lenght))
    model.add(LSTM(max_word_lenght, dropout=0.1, recurrent_dropout=0.1))
    model.add(Dense(max_word_lenght, activation='sigmoid'))
    model.add(Dense(number_of_category, activation='softmax')) #softmax used for highlight the largest values and suppress values which are significantly below the maximum value

    model.compile(loss=losses,
                optimizer=optimizers,
                metrics=['accuracy'])
    
    '''model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])'''

    return model


# In[88]:


from keras.wrappers.scikit_learn import KerasClassifier

model = KerasClassifier(build_fn=create_model, verbose=1)


# In[ ]:


# Fit the training data to the model using grid search
reg = fit_model(X_train, y_train, model)

# Produce the value for 'max_depth'
print("Parameters for the optimal model.",reg)
print(reg.get_params)

