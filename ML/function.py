from pythainlp.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
import numpy as np
def DataEncoder(encoder,dataset,encode_data):

    bar = [word_tokenize(x[0],engine='deepcut') for x in dataset ]
    bar2 = [word_tokenize(x[0],engine='deepcut') for x in [encode_data] ]
    print(bar2)
    # while 1:
    #     x=0
    bar.append(bar2[0])
    # print(bar,'bar')
    # print(bar2,'bar2')
    bar_dimension = [len(x) for x in bar2]
    encoder.fit([j for i in bar for j in i])

    encoded_Y2 = encoder.transform([j for i in bar2 for j in i] )
    text_data = []
    for x in range(len(bar2)):
        temp_data = []
        for i in range(bar_dimension[x]):
            temp_data.append(encoded_Y2[0])
            encoded_Y2 = np.delete(encoded_Y2,0)
        text_data.append(temp_data)
    return text_data
