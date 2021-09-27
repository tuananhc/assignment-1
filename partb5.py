import re
import sys
import pandas as pd
import nltk
import os
import numpy as np
import math

from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem import PorterStemmer
from preProcess import preProcess
from numpy import dot
from numpy.linalg import norm

ps = nltk.stem.PorterStemmer()
keywords = sys.argv[1:6]
keywords = [ps.stem(keyword) for keyword in keywords]  #  stem each keywords
data = pd.read_csv("partb1.csv")

curPath = os.getcwd()
#  change directory to the cricket file
filePath = os.path.abspath("cricket")
os.chdir(filePath)
fileList = sorted(list(filter(os.path.isfile, os.listdir())))

output = []  #  list of files that satisfies the conditions
vocab = []  #  vocabulary to store all stemmed words from the files with the keywords
for file in fileList:
    wordList = preProcess(file).split()
    wordList = list(map(lambda word: ps.stem(word), wordList))
    found = True
    for keyword in keywords:
        if keyword not in wordList:
            found = False
            break
    if found: 
        # add to the current list of vocab
        vocab.extend(list(set(wordList)))
        output.append(data[data["filename"] == file].values[0][1])
        
if output:
    output = pd.DataFrame({"documentID": output})
    vocab = list(set(vocab))
else:
    print("No file found contains all the keywords")
    sys.exit()

#  calculate the cosine between 2 vectors
def cosine_sim(v1, v2):
    return dot(v1, v2)/(norm(v1) * norm(v2))

scores = {}  # score dictionary for each 
termCounts = []

#  create query vector
qvector = [0] * len(vocab)
for word in keywords: 
    index = vocab.index(word)
    qvector[index] += 1
        
for doc in output["documentID"]:
    # get the filename with the corresponding document ID
    wordList = preProcess(data[data["documentID"] == doc].values[0][0]).split()
    wordList = list(map(lambda word: ps.stem(word), wordList))
    tvector = [0] * len(vocab);
    i = 0;
    # get frequency count for text vector
    for word in vocab:
        tvector[i] = wordList.count(word)
        i += 1;
    termCounts.append(tvector)
    
#  calculate the tfidf value and cosine similarity
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(termCounts)
doc_tfidf = tfidf.toarray()    
qvector = [x/math.sqrt(len(keywords)) for x in qvector]  #  getting the unit query vector
sims = [cosine_sim(qvector, doc_tfidf[d_id]) for d_id in range(doc_tfidf.shape[0])]

#  assign the cosine similarity to the corresponding file
i = 0
for doc in output["documentID"]:
    scores[doc] = format(sims[i], ".4f") # format the number to be 4 decimal places
    i += 1
    
#  sort the file according to their score in descending order
scores = {key: value for key, value in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
score = pd.DataFrame(scores.items(), columns=["documentID", "score"])
print(score)
os.chdir(curPath)
