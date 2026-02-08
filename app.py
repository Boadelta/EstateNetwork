import pymysql
import functools
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, abort, send_file
from flask_session import Session
from sqlalchemy.sql import text
from sqlalchemy import MetaData, Table, select, insert, delete
from flask_sqlalchemy import SQLAlchemy
import hashlib
import requests
import os
from io import BytesIO
from dotenv import load_dotenv

app = Flask(__name__, template_folder="templates")

username = "sql7816118"
password = "NrfY6Kk7DZ"
server = "sql7.freesqldatabase.com"
dbname = "/sql7816118"

userpass = f"mysql+pymysql://{username}:{password}@"

app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server +dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config["SQLAlCHEMY_ENGINE_OPTIONS"] ={
    'pool_pre_ping':True
}
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
#hello
db = SQLAlchemy(app)

with app.app_context():
    db.reflect()
    users = db.Table("users", db.metadata, autoload_with=db.engine)
    updates = db.Table("updates", db.metadata, autoload_with=db.engine)
    
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/dashboard')
def dashboard():
    if not session.get('name'):
        return redirect(url_for('register'))
    return render_template("dashboard.html")

@app.route('/make_post', methods=['POST'])
def make_post():
    data = request.form

    title = data['title']
    post = data['main_body'] 
    stmt = insert(updates).values(heading=title, description=post)
    db.session.execute(stmt)
    db.session.commit()
    return render_template('dashboard.html')
    
@app.route('/estateNet')
def estateNet():
    if not session.get('name'):
        return render_template('login.html')
    stmt = select(users).where(users.c.email==session.get('name'))
    mainUser = db.session.execute(stmt).fetchone()
    name = mainUser.name
    return render_template('estateNet.html', name = name)

@app.route('/tryLogin', methods=['POST'])
def tryLogin():
    data = request.form
    username = data['email']
    password = data['password']
    admt = select(users).where(users.c.email==username, users.c.password==password)
    account = db.session.execute(admt).fetchone()
    if account:
        session["name"] = username
        return redirect(url_for('estateNet'))
    else:
        msg = "Incorrect login details, try again"
    return render_template('register.html', msg = msg)

@app.route('/tryRegsiter', methods=['POST'])
def tryRegister():
    data = request.form
    
    fname = data['fname']
    lname = data['lname']
    email = data['newEmail']
    password = data['newPassword']
    phoneNo = data['phoneNo']
    name = fname + ' ' + lname
    stmt = insert(users).values(name = name, email = email, password=password, phoneNo = phoneNo)
    db.session.execute(stmt)
    db.session.commit()
    return render_template('index.html')
                    
@app.route('/editProfile')
def editProfile():
    if not session.get('name'):
        return redirect(url_for('register'))
    return render_template('editProfile.html')

@app.route('/viewProfile')
def viewProfile():
    if not session.get('name'):
        return render_template('login.html')
    stmt = select(users).where(users.c.email==session.get('name'))
    mainUser = db.session.execute(stmt).fetchone()
    name = mainUser.name
    email = mainUser.email
    phoneNo = mainUser.phoneNo
    house = mainUser.house
    role = mainUser.role
    aptType = mainUser.ApartmentType
    emergency = mainUser.EmerContName + '-' + mainUser.EmerContPhoneno
    about = mainUser.about
    return render_template('viewProfile.html', name=name, email=email, phoneNo=phoneNo, house=house, role=role, aptType = aptType, emergency=emergency, about=about)



if __name__=="__main__":
    port = int(os.environ.get("port", 5000))
    app.run(host="0.0.0.0", port = port)