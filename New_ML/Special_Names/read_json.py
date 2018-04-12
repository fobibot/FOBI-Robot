import json

# with open('PeopleInformation.json') as json_data:
with open('NameToKeyword.json') as json_data:
    python_obj = json.load(json_data)
    print(python_obj)
# print (python_obj["Teacher"]["สยาม"])
# print(python_obj["Teacher"]["สยาม"]["name"])