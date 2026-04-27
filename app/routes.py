from flask import render_template
from app import app

@app.route('/')
def home(): #main page is the login page
    return render_template('login.html')

@app.route('/explore')
def explore():
    return render_template('Explore.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/log-coffee')
def log_coffee():
    return render_template('log-coffee.html')