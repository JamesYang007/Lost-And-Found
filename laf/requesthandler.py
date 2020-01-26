from flask import Flask, render_template, request, redirect, url_for, flash
from flask import request
import geocoder

@app.route('/submit', methods=['POST'])
def submit():
    error = None
    if request.method == 'POST':
        
        title = request.files['title']
        img_file = request.files['img_file']
        imagepath = process_image(img_file)

        g = geocoder.ip('me')
        latitude = (g.latlng)[0]
        longitude = (g.latlng)[1]

        phone = phonenum_format(request.form['phone'])

        keywords = cobys_function(img_file)

        description = request.form['description']

        is_lost = request.form['is_lost']

        return add_post(title, imagepath, latitude, longitude,g phone, keywords, description, is_lost)

    else:
        error = 'Invalid post request'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('reportform.html', error=error)
 

def phonenum_format(phone_string):
    clean_num  = re.sub('[^0-9]+', '', phone_string)
    formatted_num = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(clean_num[:-1])) + clean_num[-1]
    return formatted_num

if __name__ == '__main__':
    app.run(debug=True)