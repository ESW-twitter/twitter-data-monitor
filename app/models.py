from app import db

class ActorReport(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(60))
    csv_content = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, date, csv_content):
        self.date = date
        self.csv_content = csv_content

    def __repr__(self):
        return '<ActorReport %r>' % self.id

class TweetReport(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(60))
    username = db.Column(db.String(60))
    csv_content = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, date, username, csv_content):
        self.date = date
        self.csv_content = csv_content
        self.username = username
    def __repr__(self):
        return '<TweetReport %r>' % self.id        

class RelationReport(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(60))
    csv_content = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, date, csv_content):
        self.date = date
        self.csv_content = csv_content
    def __repr__(self):
        return '<RelationReport %r>' % self.id                

class Actor(db.Model): 
    username = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, username, name):
        self.name = name
        self.username = username
    def __repr__(self):
        return '<Actor %r>' % self.username          