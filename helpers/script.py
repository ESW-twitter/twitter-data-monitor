import json
import modules
from modules.twitter_api import TwitterAPI
from modules.twitter_user import TwitterUser
from modules.csv_builder import CsvBuilder

if __name__ == '__main__':
    file = open("helpers/politicians.json")
    actors = json.load(file)
    for row in actors:
        user = TwitterUser(row["twitter_handle"])
        if user.existence == True:
            CsvBuilder.update_csv_new_autors(user)
