import csv
import os
import json
from os.path import isfile, join
            
class CsvBuilder:

    def __init__(self, header_json):
        line = ""
        for attr in header_json:
            line = line + attr['attribute'] + ";"
        line = line[:-1]    
        line = line+"\n"
        
        self.content = line
        
    def save(self, name, dir=None):
        if dir != None:
            onlydir = [f for f in os.listdir(os.getcwd()+"/results/") if not isfile(join(os.getcwd()+"/results/", f))]
            if dir not in onlydir:
                os.mkdir(os.getcwd()+"/results/"+dir)
            name = dir+"/"+name
        file = open("results/"+name+".csv", 'w')
        file.write(self.content)
        file.close


    def add_row(self, row):
        self.content = self.content+row
               

def list_to_string(list_of_words, hashtag=False):
    string = ''
    for word in list_of_words:
        if hashtag:
            string = string + '#' + str(word) + ', ' 
        else:
            string = string + str(word) + ', '
    if len(string) > 2:
        return string[:-2]
    return " "    

def list_to_row(list_of_col):
    line = ''
    for entry in list_of_col:
        line = line + str(entry) + ";"  
    line = line+"\n"

    return line