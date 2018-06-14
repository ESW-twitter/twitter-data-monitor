import pytest
import warnings
import csv
import os
import modules
import json
from modules.csv_builder import CsvBuilder, list_to_string, list_to_row, isfile


class TestFileCSV():

    def test_file_exist(self):
        header_json = json.load(open("helpers/actors_attributes.json"))
        csv = CsvBuilder(header_json)
        csv.save(name="test")
        try:
            csvfile = open(os.path.join(
                os.path.dirname(__file__), '../results/test.csv'))
            csvfile.close()
            arquivo = True
        except:
            arquivo = False
        assert arquivo == True

    def test_list_to_row(self):
        vector = ['SolidariedadeInternacional', 30,
                  '3', 'DemarcaçãoJá', 'qualquercoisa']
        row = list_to_row(vector)
        assert row == "SolidariedadeInternacional;30;3;DemarcaçãoJá;qualquercoisa;\n"

    def test_list_to_string(self):
        vector = ['SolidariedadeInternacional', 'DemocratizeJá',
                  'LulapeloBrasil', 'DemarcaçãoJá', 'OcupaCuritiba']
        hashtags = list_to_string(vector, hashtag=True)
        assert "#SolidariedadeInternacional" in hashtags
        assert "#DemocratizeJá" in hashtags

    def test_save(self):
        vector = CsvBuilder
        vector.content = str(
            ['SolidariedadeInternacional', 30, '3', 'DemarcaçãoJá', 'qualquercoisa'])
        test1 = "test1"
        CsvBuilder.save(vector, test1, None)
        assert isfile("results/"+test1+".csv")
