import re
import sys
import pandas as pd
import nltk
import os

from nltk.stem import PorterStemmer
from preProcess import preProcess

ps = nltk.stem.PorterStemmer()
#  get 5 keywords at max
keywords = sys.argv[1:6]

#  stem all keywords
keywords = [ps.stem(keyword) for keyword in keywords]
data = pd.read_csv("partb1.csv")

curPath = os.getcwd()
filePath = os.path.abspath("cricket")
os.chdir(filePath)
fileList = sorted(list(filter(os.path.isfile, os.listdir())))

output = []
for file in fileList:
    wordList = preProcess(file).split()
    #  stem every word in the file
    wordList = list(map(lambda x: ps.stem(x), wordList))
    found = True
    for keyword in keywords:
        if keyword not in wordList:
            found = False
            break
    if found: 
        output.append(data[data["filename"] == file].values[0][1])
        
if output:
    output = pd.DataFrame({"documentID": output})
    print(output)
else:
    print("No file found contains all the keywords")
   
os.chdir(curPath)
