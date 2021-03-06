from flask import Flask, render_template, url_for, flash, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from flask import request
from flask_sqlalchemy import SQLAlchemy
import geocoder
import os
import imgprocess
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/post.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

######################################################
# Database Types
######################################################

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    imagepath = db.Column(db.String(100))
    #uni = db.Column(db.String(20))
    phone = db.Column(db.String(15)) # should it be String or Integer?
    #keywords = db.Column(db.String(100))
    desc = db.Column(db.String(1000))
    lost = db.Column(db.Boolean)

class Coordinate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reportform.html')
def reportform():
    return render_template('reportform.html')

@app.route('/submit', methods=['POST'])
def submit():
    error = None
    if request.method == 'POST':

        uniquepath = imgprocess.process_image(request.files['item_photo'])
        print(uniquepath)
        params = {
            "title" : request.form['title'],
            "imagepath" : uniquepath,
            "phone" :  phonenum_format(request.form['phone']),
            "desc" : request.form['description'],
            "lost" : bool(request.form['is_lost'])
        }

        print("entering form fields for-loop")
        for prop in request.form.items():
            print(prop)

        print("entering files for-loop")
        for prop in request.files.items():
            print(prop)

        f = request.files["item_photo"]
        print(f)
        f.save(uniquepath)

        # TODO: get ip of requester
        # create another db for latitude and longitude
        #g = geocoder.ip('me')
        #latitude = (g.latlng)[0]
        #longitude = (g.latlng)[1]

        #keywords = cobys_function(img_file)

        post = Post(**params)

        # TODO: add Coordinate object with all coordinates

        db.session.add(post)
        db.session.commit()
        return render_template('index.html')

    else:
        error = 'Invalid post request'

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    #return render_template('reportform.html', error=error)

def phonenum_format(phone_string):
    clean_num  = re.sub('[^0-9]+', '', phone_string)
    formatted_num = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(clean_num[:-1])) + clean_num[-1]
    return formatted_num

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
