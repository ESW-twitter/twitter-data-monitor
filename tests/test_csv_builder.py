import unittest
import warnings
import csv
import os
import modules
from modules.csv_builder import CsvBuilder

class TestFileCSV(unittest.TestCase):
    def test_file_exist(self):
        try:
            csvfile = open(os.path.join(os.path.dirname(__file__),'../results/teste.csv'))
            csvfile.close()
            arquivo = True
        except:
            arquivo = False
        self.assertEqual(True, arquivo)

    def test_create_csv(self):
        CsvBuilder.create_csv_basic('teste')
        with open(os.path.join(os.path.dirname(__file__),'../results/teste.csv'), 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            row1 = next(reader)
            first_row = ["nome", "seguidores", "tweets", "seguindo", "curtidas","retweets", "favorites", "hashtags", "mentions"]
            self.assertEqual(first_row,row1)
            csvfile.close()

    def test_word_separator(self):
        vector = ['SolidariedadeInternacional', 'DemocratizeJá', 'LulapeloBrasil','DemarcaçãoJá','OcupaCuritiba']
        string = '#SolidariedadeInternacional #DemocratizeJá #LulapeloBrasil #DemarcaçãoJá #OcupaCuritiba '
        hashtags = CsvBuilder.word_separator(vector, hashtag=True)
        self.assertEqual(string,hashtags)

if __name__ == '__main__':
    unittest.main()
