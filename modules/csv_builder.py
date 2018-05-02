import csv
import os
# from twitter_user import TwitterUser

class CsvBuilder:

    @staticmethod
    def create_csv_basic():
        with open(os.path.join(os.path.dirname(__file__), 'results/autores.csv'), 'w+') as csvfile:
            writer_t = csv.writer(csvfile, delimiter=';')
            writer_t.writerow(["nome", "seguidores", "tweets", "seguindo", "curtidas", "hashtags"])
            csvfile.close()

    @staticmethod
    def update_csv_new_autors(user):
        hashtag = TwitterUser.last_month_hashtags(user)
        with open(os.path.join(os.path.dirname(__file__),'results/autores.csv'), 'a') as csvfile:
            writer_t = csv.writer(csvfile, delimiter=';')
            writer_t.writerow([user.name, user.followers_count,
            user.tweets_count, user.following_count, user.likes_count, CsvBuilder.word_separator(hashtag)])
            csvfile.close()

    @staticmethod
    def word_separator(hashtag):
        row = ''
        if len(hashtag) != 0:
            for word in hashtag:
                word = '#' + word + ' '
                row = row + word
        return row
