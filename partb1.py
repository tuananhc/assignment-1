## Part B Task 

import re
import pandas as pd
import os
import argparse

re.DOTALL

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()

curPath = os.getcwd()
#  change to the cricket directory
filePath = os.path.abspath("cricket")
os.chdir(filePath)

fileList = sorted(list(filter(os.path.isfile, os.listdir())))
docIDs = []
for file in fileList:
    f = open(file)
    result = re.findall(r'[A-Z]{4}\-\d{3}.{0,2}', f.read())
    
    #  no extra character after numbers
    if len(result[0]) == 8:
        docIDs.append(result[0])
        
    #  1 extra character is found
    elif len(result[0]) == 9:
        if (result[0][-1]).isupper():
            docIDs.append(result[0])
        #  if not an uppercase character, discard it
        else:
            docIDs.append(result[0][:-1])
            
    #  2 extra characters are found
    else:
        #  take 1 extra uppercase character if there are 2 of them
        if result[0][-2].isupper() and result[0][-1].isupper():
            docIDs.append(result[0][:-1])
        #  else discard it
        else:
            docIDs.append(result[0][:-2])
    f.close()
        
os.chdir(curPath)
columns = {"filename": fileList, "documentID": docIDs}
data = pd.DataFrame(columns)
data.to_csv(args.filename, index=False)
