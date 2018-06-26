import pytest
import warnings
import csv
import os
import modules
import json
from modules.csv_builder import CsvBuilder, list_to_string , list_to_row

class TestFileCSV():

    def test_file_exist(self):
        header_json = json.load(open("helpers/actors_attributes.json"))
        csv = CsvBuilder(header_json)
        csv.save(name = "tests/test")
        try:    
            csvfile = open('tests/test.csv')
            csvfile.close()
            arquivo = True
        except:
            arquivo = False
        assert arquivo == True

    def test_list_to_row(self):
        vector = ['SolidariedadeInternacional', 30 , '3','DemarcaçãoJá','qualquercoisa']
        row = list_to_row(vector)
        assert row == "SolidariedadeInternacional;30;3;DemarcaçãoJá;qualquercoisa;\n" 
       
    def test_list_to_string(self):
        vector = ['SolidariedadeInternacional', 'DemocratizeJá', 'LulapeloBrasil','DemarcaçãoJá','OcupaCuritiba']
        hashtags = list_to_string(vector, hashtag=True)
        assert "#SolidariedadeInternacional" in hashtags
        assert "#DemocratizeJá" in hashtags
        
    
