import csv
import os
# from twitter_user import TwitterUser

class CsvBuilder:

    @staticmethod
    def create_csv_basic(name):
        with open(os.path.join(os.path.dirname(__file__), '../results/'+name+".csv"), 'w+') as csvfile:
            writer_t = csv.writer(csvfile, delimiter=';')
            writer_t.writerow(["nome", "seguidores", "tweets", "seguindo", "curtidas","retweets", "favorites", "hashtags", "mentions"])
            csvfile.close()

    @staticmethod
    def update_csv_new_autors(name, user):
        with open(os.path.join(os.path.dirname(__file__),'../results/'+name+".csv"), 'a') as csvfile:
            writer_t = csv.writer(csvfile, delimiter=';')
            writer_t.writerow([user.name, user.followers_count,
            user.tweets_count, user.following_count, user.likes_count, user.retweets_count, user.favorites_count, CsvBuilder.word_separator(user.hashtags, hashtag=True),CsvBuilder.word_separator(user.mentions) ])
            csvfile.close()

    @staticmethod
    def word_separator(word_list, hashtag=False):
        row = ''
        for word in word_list:
            if hashtag:
                word = '#' + word + ' '
            else:
                word = word + ' ' 
            row = row + word
    
        return row
