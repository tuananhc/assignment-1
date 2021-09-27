# Part B Task 2
import re
import os
import sys

#  the function preProcess is included on the GitHub repository
from preProcess import preProcess

curPath = os.getcwd()
#  first path is the name of the intended directory
filePath = os.path.abspath(sys.argv[1][:7])
os.chdir(filePath)
   
#  last path is the name of the file itself
sys.stdout.write(preProcess(sys.argv[1][7:]))
os.chdir(curPath)
