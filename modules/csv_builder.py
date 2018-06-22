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
        
    def save(self, name):
        file = open(name+".csv", 'w')
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