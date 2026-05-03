from flask import flash, redirect, render_template, url_for
from app import app, db
from app.forms import CoffeeLogForm
import os

from app.models import CoffeeLog

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
    form = CoffeeLogForm()
    if form.validate_on_submit():
        #handle photo upload
        photo = form.photo.data
        photo_filename = photo.filename
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
        photo_path = f'uploads/{photo_filename}'

        #saving user input to database
        entry = CoffeeLog(
            cafe_name=form.cafe_name.data,
            coffee_type=form.coffee_type.data,
            rating=form.rating.data,
            photo_path=photo_path,
            notes=form.notes.data)
        db.session.add(entry)
        db.session.commit()

        flash('Coffee logged successfully!')
        return redirect(url_for('my_journal')) #go to the journal page after coffee logged
    return render_template('log-coffee.html', title='Log a Coffee', form=form) #render the log-coffee page with the form for user input
        
        