from app import db

class ActorReport(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30))
    hour = db.Column(db.String(30))
    csv_content = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, date, hour, csv_content):
        self.date = date
        self.hour = hour
        self.csv_content = csv_content

    def __repr__(self):
        return '<ActorReport %r>' % self.id

class TweetReport(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30))
    hour = db.Column(db.String(30))
    actor_id = db.Column(db.String(32))
    csv_content = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, date, hour, actor_id, csv_content):
        self.date = date
        self.csv_content = csv_content
        self.actor_id = actor_id
        self.hour = hour
    
    def __repr__(self):
        return '<TweetReport %r>' % self.id        

class RelationReport(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30))
    hour = db.Column(db.String(30))
    csv_content = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, date, hour, csv_content):
        self.date = date
        self.hour = hour
        self.csv_content = csv_content
    def __repr__(self):
        return '<RelationReport %r>' % self.id                

class Actor(db.Model): 
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(60))
    name = db.Column(db.String(60))

    def __init__(self, id,  username, name):
        self.id = id
        self.name = name
        self.username = username
    
    def __repr__(self):
        return '<Actor %r>' % self.id

