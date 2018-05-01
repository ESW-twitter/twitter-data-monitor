from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'jdbc:mysql://localhost:3306/twitter_db'
db = SQLAlchemy(app)

class Report(db.model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    csv_content = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<Report %r>' % self.id

@app.route('/')
def hello_world():
   return 'Hello World'

if __name__ == '__main__':
    app.run()
