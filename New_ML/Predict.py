from pythainlp.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
from keras.preprocessing import sequence
import pandas
import numpy as np
import time as t

class Prediction:
    def __init__(self, confidence_value):
        self.encoder_input = LabelEncoder()
        self.encoder_output = LabelEncoder()
        self.model = None

        self.confidence_value = confidence_value

        print("Loading Model..")
        self.LoadModel()
        print("Finished Loading Model")

    def LoadModel(self):
        # dataframe = pandas.read_csv("New_ML/Datasets_NewLabel.csv", header=None)
        # dataset = dataframe.values

        self.encoder_input.classes_ = np.load('New_ML/Saved_Model/Encoded_Input_classes.npy')
        self.encoder_output.classes_ = np.load('New_ML/Saved_Model/Encoded_Output_classes.npy')

        self.model = load_model('New_ML/Saved_Model/model.h5')

    def TransformInputData2EncodeValue(self, _input, _max_word_lenght=30):
        sentence = []
        for word in _input:
            try: # New words handler
                temp = list(self.encoder_input.transform([word]))
                sentence += temp
            except ValueError:
                # print(("*"*10), "No", word, "in database", ("*"*10))
                pass
        
        encoded_sentence = sequence.pad_sequences([sentence], maxlen=_max_word_lenght)
        # print(encoded_sentence)

        return encoded_sentence

    def Predict_Manual(self, listen_func):
        while 1:
            sentence = input("Sentence : ")
            if sentence == "1":
                sentence = listen_func()
                last = t.time()
                words = word_tokenize(sentence, engine='deepcut') #wait for input sentence by typing
                print("Word Segmentation time :", t.time()-last)
                
                last = t.time()
                encoded_sentence = self.TransformInputData2EncodeValue(words)
                print("Encode Data time :", t.time()-last)

                # Predict output
                last = t.time()
                predictions = self.model.predict(encoded_sentence).tolist()
                print("Predict time :", t.time()-last)
                print(predictions)

                last = t.time()
                predicted = self.encoder_output.inverse_transform([predictions[0].index(max(predictions[0]))])
                print("Decoded Predict time :", t.time()-last)
                print(predicted)

    def Predict(self, sentence):
        last = t.time()
        words = word_tokenize(sentence, engine='deepcut') #wait for input sentence by typing
        if __debug__:
            print("Word Segmentation time :", t.time()-last)
        
        last = t.time()
        encoded_sentence = self.TransformInputData2EncodeValue(words)
        if __debug__:
            print("Encode Data time :", t.time()-last)

        # Predict output
        last = t.time()
        predictions = self.model.predict(encoded_sentence).tolist()
        if __debug__:
            print("Predict time :", t.time()-last)
            print("Prediction Score", predictions)
            print("Max Prediction Score", max(predictions[0]))

        last = t.time()
        predicted = self.encoder_output.inverse_transform([predictions[0].index(max(predictions[0]))])
        if __debug__:
            print("Decoded Predict time :", t.time()-last)
            print("Predicted as : ", predicted) if max(predictions[0]) >= self.confidence_value else print("Predicted as : Low Confidence")

        return predicted[0] if max(predictions[0]) >= self.confidence_value else None # Prediction threshold >= 0.75 or 75%

