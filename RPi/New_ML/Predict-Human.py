from pythainlp.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
from keras.preprocessing import sequence
import pandas
import numpy as np

dataframe = pandas.read_csv("Datasets_NewLabel.csv", header=None)
dataset = dataframe.values


encoder_input = LabelEncoder()
encoder_input.classes_ = np.load('Saved_Model/Encoded_Input_classes-Human.npy')

encoder_output = LabelEncoder()
encoder_output.classes_ = np.load('Saved_Model/Encoded_Output_classes-Human.npy')

model = load_model('Saved_Model/Human-model.h5')

def TransformInputData2EncodeValue(_input, _max_word_lenght=30):
    sentence = []
    for word in _input:
        try: # New words handler
            temp = list(encoder_input.transform([word]))
            sentence += temp
        except ValueError:
            print(("*"*10), "No", word, "in database", ("*"*10))
            pass
    
    encoded_sentence = sequence.pad_sequences([sentence], maxlen=_max_word_lenght)
    print(encoded_sentence)

    return encoded_sentence

words = word_tokenize("อ.อยู่ชั้นไหน", engine='deepcut')
encoded_sentence = TransformInputData2EncodeValue(words)

# Predict output
predictions = model.predict(encoded_sentence).tolist()
print(predictions)
predicted = encoder_output.inverse_transform([predictions[0].index(max(predictions[0]))])
print(predicted)


