import csv
import os
import json
from modules.twitter_user import TwitterUser
from modules.__init__ import Report

def generate_csv_report():
    csv_content = "nome;seguidores;tweets;seguindo;curtidas;hashtags\n"
    file = open("./helpers/politicians.json")
    actors = json.load(file)
    for row in actors:
        user = TwitterUser(row["twitter_handle"])
        if user.existence == True:
            aux = user.name,";",user.followers_count,";",user.tweets_count,";",
            user.following_count,";",user.likes_count,";\n"
            csv_content = csv_content + aux

    print(csv_content)

if __name__ == '__main__':
    generate_csv_report()
