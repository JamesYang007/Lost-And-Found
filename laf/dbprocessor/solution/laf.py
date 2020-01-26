from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class laf(db.Model):
     # image path (unique ID.jpeg), locations, contact info (uni), phone#, keywords, desc, lost

     imagepath = db.Column(db.String(100))
     latitude = db.Column(db.Double)
     longitude = db.Column(db.Double)
     uni = db.Column(db.String(20))
     phone = db.Column(db.String(15)) # should it be String or Integer?
     keywords = db.Column(db.String(100))
     desc = db.Column(db.String(1000))
     lost = db.Column(db.Boolean)
