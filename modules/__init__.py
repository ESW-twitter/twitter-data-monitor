from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:password@localhost/twitter_db"
db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    csv_content = db.Column(db.LargeBinary)

    def __init__(self, date, csv_content):
        self.date = date
        self.csv_content = csv_content

    def __repr__(self):
        return '<Report %r>' % self.id

@app.route('/')
def hello_world():
   return 'Hello World'

if __name__ == '__main__':
    app.run()
