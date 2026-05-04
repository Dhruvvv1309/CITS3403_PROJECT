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

@app.route('/my_journal')
def my_journal():
    return render_template('my_journal.html')

@app.route('/log-coffee')
def log_coffee():
    return render_template('log-coffee.html')

@app.route('/game')
def game():
    return render_template('game.html')