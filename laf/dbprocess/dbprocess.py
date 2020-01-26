from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# create a global variable of the object Laf inside this file.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagepath = db.Column(db.String(100))
    #latitude = db.Column(db.Double)
    #longitude = db.Column(db.Double)
    #uni = db.Column(db.String(20))
    #phone = db.Column(db.String(15)) # should it be String or Integer?
    #keywords = db.Column(db.String(100))
    desc = db.Column(db.String(1000))
    #lost = db.Column(db.Boolean)

# function goes here. I take in an Object and set the model fields based on the attributes of the given object

@app.route('/')
def index():
    return redirect(url_for('index'))

def add_post(imagepath,
             #latitude,
             #longitude,
             #uni,
             #phone,
             #keywords,
             desc
             #lost
             ):

    params = {
        "imagepath" : imagepath,
        "desc" : desc
    }

    entry = Entry(**params)
    db.session.add(entry)
    db.session.commit()
    #return redirect(url_for('index')) # stay on the home page

## Route to index (default) page with blank database.
#@app.route('/')
#def index():
#    lost = Todo.query.filter_by(lost = True).all()
#    found = Todo.query.filter_by(lost = False).all()
#
#    return render_template('index.html',
#       incomplete = incomplete, complete = complete)
#
## Route used to add items to the database.
#    db.session.add(todo)
#    db.session.commit()
#
#    return redirect(url_for('index')) # stay on the home page

if __name__ == '__main__':
    app.run(debug=True)
    add_post('./hello', 'some description')
