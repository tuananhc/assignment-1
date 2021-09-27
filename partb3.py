import re
import sys
import pandas as pd
import nltk
import os

from preProcess import preProcess

data = pd.read_csv("partb1.csv")
#  get at most 5 keywords
keywords = sys.argv[1:6]

curPath = os.getcwd()
filePath = os.path.abspath("cricket")
os.chdir(filePath)
fileList = sorted(list(filter(os.path.isfile, os.listdir())))

output = []
for file in fileList:
    text = preProcess(file)
    text = text.split()
    found = True
    for keyword in keywords:
        if keyword not in text:
            found = False
            break
    #  if all keywords are found, add the document ID of the file
    if found: 
        output.append(data[data["filename"] == file].values[0][1])

if output:
    output = pd.DataFrame({"documentID": output})
    print(output)
else:
    print("No file found contains all the keywords")
os.chdir(curPath)
