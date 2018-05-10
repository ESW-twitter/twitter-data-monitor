import pytest
import warnings
import csv
import os
import modules
from modules.csv_builder import CsvBuilder

class TestFileCSV():
    def test_file_exist(self):
        try:
            csvfile = open(os.path.join(os.path.dirname(__file__),'../results/teste.csv'))
            csvfile.close()
            arquivo = True
        except:
            arquivo = False
        assert arquivo == True

    def test_create_csv(self):
        CsvBuilder.create_csv_basic('teste')
        with open(os.path.join(os.path.dirname(__file__),'../results/teste.csv'), 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            row1 = next(reader)
            first_row = ["nome", "seguidores", "tweets", "seguindo", "curtidas","retweets", "favorites", "hashtags", "mentions"]
            assert first_row == row1

            csvfile.close()

    def test_list_to_string(self):
        vector = ['SolidariedadeInternacional', 'DemocratizeJá', 'LulapeloBrasil','DemarcaçãoJá','OcupaCuritiba']
        vector = [[x,1] for x in vector]
        string = '#SolidariedadeInternacional,1 #DemocratizeJá,1 #LulapeloBrasil,1 #DemarcaçãoJá,1 #OcupaCuritiba,1 '
        hashtags = CsvBuilder.list_to_string(vector, hashtag=True)
        assert string == hashtags

