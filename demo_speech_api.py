# import FOBI
# import time as t

# robot = FOBI.Robot()

# while 1:
#     for i in range(3,0,-1):
#         print(i)
#         t.sleep(1)
#     sentence = robot.Listen()
#     print(sentence)

from pythainlp.tokenize import word_tokenize

while 1:
    print(word_tokenize(input("Sentence :"), engine='deepcut'))