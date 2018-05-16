import pytest
import warnings
import csv
import os
import modules
from modules.csv_builder import CsvBuilder, list_to_string

class TestFileCSV():

    def test_file_exist(self):
        try:
            csvfile = open(os.path.join(os.path.dirname(__file__),'../results/teste.csv'))
            csvfile.close()
            arquivo = True
        except:
            arquivo = False
        assert arquivo == True

    def test_list_to_string(self):
        vector = ['SolidariedadeInternacional', 'DemocratizeJá', 'LulapeloBrasil','DemarcaçãoJá','OcupaCuritiba']
        hashtags = list_to_string(vector, hashtag=True)
        assert "#SolidariedadeInternacional" in hashtags
        assert "#DemocratizeJá" in hashtags
