import re

def preProcess(filename):
    f = open(filename, "r")
    output = re.sub(r"[A-Z]{1}", lambda x: x[0].lower(), f.read())
    output = re.sub(r"\d", "", output)
    output = re.sub(r"\W", " ", output)
    output = re.sub(r"\s+", " ", output)
    return output
