import sys
import os
import modules
import json
from datetime import datetime, timedelta
from modules.twitter_api import TwitterAPI
from modules.twitter_user import TwitterUser
from modules.csv_builder import CsvBuilder

if __name__ == '__main__':
    file = open("helpers/politicians.json")
    actors = json.load(file)

    if len(sys.argv) == 4:
        day = int(sys.argv[1])
        month = int(sys.argv[2])
        year = int(sys.argv[3])
    else:    
        try:
            files = [x for x in os.listdir("results/") if x!="teste.csv"]
            files.sort(reverse=True)
            last_capture = files[0].split(" ")[0].split("-")  
            day = int(last_capture[2])
            month = int(last_capture[1])
            year = int(last_capture[0])
        except Exception as e:
            yesterday = datetime.now() - timedelta(days=1)
            day = yesterday.day
            month = yesterday.month
            year = yesterday.year


    print("Collecting information from "+str(year)+"/"+str(month)+"/"+str(day)+" to date")        

    name = str(datetime.now())+"-from-"+str(year)+"-"+str(month)+"-"+str(day)
    CsvBuilder.create_csv_basic(name)
    for row in actors:
        user = TwitterUser(row["twitter_handle"])
        if user.existence == True:
            user.retrieve_info_from(day, month, year)
            print("Retrieving information of "+ str(user.username))
            CsvBuilder.update_csv_new_autors(name, user)
