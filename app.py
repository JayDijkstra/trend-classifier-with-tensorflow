from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
import sqlite3 as sql
import subprocess
from werkzeug.utils import secure_filename
import time
import os
import pprint
import sys
import io

#Declare our Flask Application
app = Flask(__name__)
#Create variable containing values to store uploaded images. Tmp folder in project
UPLOAD_FOLDER = 'static/images/tmp/'
#Because of the working of tensorflow it is not yet allowed to use other extension then jpeg, jpg
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
#Configure our app to use our chosen upload Folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#query handler in an Python shell
pythonQuery = "python trendthis.py static/images/tmp/"

#create a Global output variable for storing our prediction
global output

#Routes for different pages.. always needs to return a value (or a Template)
@app.route('/')
def homepage():
    return render_template("template.html")

#Registration Handler for Python registration to SQLite db
@app.route('/register', methods=["GET", "POST"])
def register():
    #create a global connection var
    global con
    #check if the request from the form is POST.
    if request.method == 'POST':
        try:
            #try to fill variables with input data from the form
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            password = request.form['password']
            bsrcolor = request.form['bsrcolor']
            #create a connection with the sql database.
            with sql.connect("database.db") as con:
                #create a cursor to scroll through the rows.
                cur = con.cursor()
                #execute the query to insert the input data in the database.
                cur.execute("INSERT INTO users(firstname,lastname,email,password,bsrcolor) VALUES (?,?,?,?,?)", (firstname,lastname,email,password,bsrcolor))
                #commit the data to the database.
                con.commit()
                #after succesfull redirect the user to the template.html file.
                return render_template('template.html')
        #if there is an error give the user an exception.
        except Exception as e:
            return str(e)

#A function to check if the extension of an image is in the ALLOWED_EXTENSIONS var. For this Application there is only made use of JPG and JPEG.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#Set Up a Route from Python Flask
@app.route('/', methods=['GET', 'POST'])
#function to upload a file to the database
def upload_file():
    #create a global variable fileName.
    global fileName;
    #check if the request method from the form is post
    if request.method == 'POST':
        #if the file is not an File. Notify the user.
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        #if the file is a file but dont have a filename.
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        #if the file has the allowed extension (in our example JPEG or JPG)
        if file and allowed_file(file.filename):
            #secure the file name
            filename = secure_filename(file.filename)
            #set the filename to the secured string
            fileName = str(filename)
            #save the file in the upload folder, in this example /static/images/tmp
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #set the output to query a Python shell command on the newly created file to classify.
            output = subprocess.getoutput(pythonQuery + fileName)
            try:
                #set all values in a database to to store the newly created trend
                #the python shell automaticly adds the classification (Magic Card,
                #fidget spinner or segway as classification)
                trend = output
                filename = filename
                bsrcolor = request.form['bsrcolor']
                description = request.form['description']
                tag = request.form['tag']
                redvotes = 0
                bluevotes = 0
                yellowvotes = 0
                greenvotes = 0
                teachervote = 0
                hottness = "not"

                #make a connection to the database
                with sql.connect("database.db") as con:
                    #create a cursor to scroll trough the rows.
                    cur = con.cursor()
                    #execute the query to insert the newly trend.
                    cur.execute("INSERT INTO images(trend,filename, bsrcolor, description,tag,redvotes,bluevotes,yellowvotes,greenvotes,teachervote,hottness) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (trend, filename, bsrcolor,description,tag,redvotes,bluevotes,yellowvotes,greenvotes,teachervote,hottness))
                    #commit the query.
                    con.commit()
            #if there is an error, return this to the user.
            except Exception as e:
                return str(e)

            #make an connection to the database.
            con = sql.connect("database.db")
            #make an factory of the SQL rows.
            con.row_factory = sql.Row

            #create an cursor to scroll trough the Rows.
            cur = con.cursor()
            #execute a Query to get a file that is identified as the same TREND to return to the user.
            cur.execute("select * from images where trend like ? and tag like ? and filename not like  ? ORDER BY RANDOM() LIMIT 1",('%'+output+'%', tag, filename))
            #get all the rows from the trend.
            rows = cur.fetchall()
            #render the trend back to the user to give the user the ability to vote how much this trend is simular to the just uploaded trend.
            return render_template('vote.html',rows=rows)

    # return render_template('upload.html')
if __name__ == '__main__':
    app.run(debug=True)
    app.secret_key = 'futurebaseprototype'
