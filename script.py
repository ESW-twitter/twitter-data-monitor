import sys
import os
import modules
import json
from datetime import datetime, timedelta
from modules.twitter_api import TwitterAPI
from modules.twitter_user import TwitterUser
from modules.csv_builder import CsvBuilder


# basically, you can type 'python3 script.py day month year' in the command line, which will perform a capture since the day you specified to the current day.
# example: 'python3 script.py 1 5 2018' will do a search from may 1 2018 to today, and generate a .csv
# if you simply type 'python3 script.py' it will look for the most recent capture in the 'results' folder and start the capture from it.
# if nothing is found in the 'results' folder, it will perform the search from one day before the current date.


if __name__ == '__main__':
    file = open("helpers/politicians.json")
    actors = json.load(file)

    if len(sys.argv) == 4:
        day = int(sys.argv[1])
        month = int(sys.argv[2])
        year = int(sys.argv[3])
        hour=0
        minute=0
    else:    
        try:
            files = [x for x in os.listdir("results/") if x!="teste.csv"]
            files.sort(reverse=True)
            last_capture = files[0].split(" ")[0].split("-")  
            day = int(last_capture[2])
            month = int(last_capture[1])
            year = int(last_capture[0])
            day_hour = files[0].split(" ")[1].split(":")
            hour = int(day_hour[0])
            minute= int(day_hour[1])
        except Exception as e:
            yesterday = datetime.utcnow() - timedelta(days=1)
            day = yesterday.day
            month = yesterday.month
            year = yesterday.year
            hour = 0
            minute = 0


    print("Collecting information from "+str(year)+"/"+str(month)+"/"+str(day)+" "+str(hour)+":"+str(minute)+" to date")        

    name = str(datetime.utcnow())+"-from-"+str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)
    CsvBuilder.create_csv_basic(name)
    for row in actors:
        user = TwitterUser(row["twitter_handle"])
        if user.existence == True:
            print("Retrieving information of "+ str(user.username))
            user.retrieve_info_from(day, month, year, hour, minute)
            CsvBuilder.update_csv_new_autors(name, user)
