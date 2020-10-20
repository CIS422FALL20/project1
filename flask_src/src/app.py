from flask import Flask, request, render_template, make_response, url_for, redirect
from werkzeug.utils import secure_filename
import os
from google import testing_importing_gpx



# Instantiate the app
app = Flask(__name__)
#config = configparser.ConfigParser()
#config.read("credentials.ini")
ALLOWED_EXTENSIONS = set(['gpx'])


# Helper Function
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/viewfile/<filename>')
def viewfile(filename):
    return testing_importing_gpx(filename)


"""Login Page Logic"""
@app.route("/", methods=["GET", "POST"])
def get():
    if request.method == 'POST':
        file_ = request.files['submitted_data']
        if file_.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file_ and allowed_file(file_.filename):
            filename = secure_filename(file_.filename)
            file_.save(filename)
            return redirect(url_for('viewfile', filename=filename))
        elif file_ and not allowed_file(file_.filename):
            return "Only gpx files allowed, go back and enter a gpx file"
    return render_template('submit_data.html')


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
