import Speech
import json
import time as t

def LoadJsonFile(filename):
    try:
        with open(filename) as json_data:
            json_file = json.load(json_data)
    except:
        print("No file name", filename, ".json")
        pass
    return json_file

NameToKeyword = LoadJsonFile('New_ML/Special_Names/NameToKeyword.json')
Speech = Speech.Speech(list(NameToKeyword.keys()))

# Speech.CalibrateMicNoiseThreshold()

while True:
    print("Listening...")
    sentence = Speech.listen_to_gcloud()
    t.sleep(2)
