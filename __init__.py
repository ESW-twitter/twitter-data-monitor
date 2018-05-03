import csv
import os
import json
import datetime
from modules.twitter_user import TwitterUser
from modules.__init__ import Report
from modules.__init__ import db

def generate_csv_report():
    csv_content = "nome;seguidores;tweets;seguindo;curtidas;hashtags;\n"
    file = open("helpers/politicians.json")
    actors = json.load(file)
    for row in actors:
        user = TwitterUser(row["twitter_handle"])
        if user.existence == True:
            aux = "{};{};{};{};{};\n".format(user.name, user.followers_count, user.tweets_count, user.following_count, user.likes_count)
            csv_content = csv_content + aux
    # print(csv_content)
    f = Report(datetime.datetime.now().strftime('%d/%m/%Y'), csv_content.encode())
    db.session.add(f)
    db.session.commit()


if __name__ == '__main__':
    generate_csv_report()
