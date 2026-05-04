from flask import flash, redirect, render_template, url_for
from app import app
from app.forms import CoffeeLogForm

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

@app.route('/log-coffee', methods=['GET', 'POST'])
def log_coffee():
    form=CoffeeLogForm()
    if form.validate_on_submit():
        #save to database once connected
        flash('Coffee logged successfully!')
        return redirect(url_for('my_journal'))
    return render_template('log-coffee.html', title='Log a Coffee', form=form)
        
        