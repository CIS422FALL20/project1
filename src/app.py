from flask import Flask, send_file, flash, request, render_template, make_response, url_for, redirect
from werkzeug.utils import secure_filename
import os
import time
from main import main
import logging



# Instantiate the app
app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['gpx'])
app.secret_key = 'Yeehaw'


# Helper Function
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/viewfile/<filename>')
def viewfile(filename):
    app.logger.info('In viewfile!')
    loop = main(filename)
    for elem in loop:
        if len(elem) > 0:
            address = elem[3].street
            if elem[0] == '0':
                flash('Starting on ' + str(address))
            else:
                turn_direct = elem[1]
                distance = round(elem[2], 2)
                if distance < 1001:
                    distance = int(distance)
                    flash("In " + str(distance) + "m turn " + str(turn_direct) + " on "+ str(address))
                else:
                    distance = round(float(distance/1000), 1)
                    flash("In " + str(distance) + "km turn " + str(turn_direct) + " on "+ str(address))
    return render_template('submit_data.html') 


"""Login Page Logic"""
@app.route("/", methods=["GET", "POST"])
def get():
    if request.method == 'POST':
        file_ = request.files['submitted_data']
        if file_.filename == '':
            return 'No file selected! Enter a gpx file'

        if file_ and allowed_file(file_.filename):
            filename = secure_filename(file_.filename)
            file_.save(filename)
            app.logger.info('Computing turns!')
            return redirect(url_for('viewfile', filename=filename))

        elif file_ and not allowed_file(file_.filename):
            return "Only gpx files allowed, go back and enter a gpx file"

    app.logger.info('submit page!')
    return render_template('submit_data.html')


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
