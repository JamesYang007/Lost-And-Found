from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# create a global variable of the object Laf inside this file.

lafobj = laf()

# function goes here. I take in an Object and set the model fields based on the attributes of the given object

def add_post(imagepath, latitude, longitude, uni, phone, keywords, desc, lost):
    lafobj = laf(laf.imagepath = imagepath, laf.latitude = latitude, laf.longitude = longitude, laf.uni = uni, laf.phone = phone, laf.keywords = keywords, laf.desc = desc, laf.lost = lost)
    db.session.add(lafobj)

    return redirect(url_for('index')) # stay on the home page

# Route to index (default) page with blank database.
@app.route('/')
def index():
    lost = Todo.query.filter_by(lost = True).all()
    found = Todo.query.filter_by(lost = False).all()

    return render_template('index.html',
       incomplete = incomplete, complete = complete)

# Route used to add items to the database.
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index')) # stay on the home page

if __name__ == '__main__':
    app.run(debug = True)
