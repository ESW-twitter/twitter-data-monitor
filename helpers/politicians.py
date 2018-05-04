import csv
with open('helpers/groups_file.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("{\"name\":" + "\"" + row["FRENTES / COLETIVOS"] + "\",\"twitter_handle\":" + "\"" + row["TWITTER"] + "\"},")
