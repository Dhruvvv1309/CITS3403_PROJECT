from flask import flash, redirect, render_template, url_for
from app import app, db
from app.forms import CoffeeLogForm
import os

from app.models import CoffeeLog

def _rating_stars(rating):
    rating = int(rating or 0)
    rating = max(0, min(rating, 5))
    return '★' * rating + '☆' * (5 - rating)

def _coffee_type_label(coffee_type):
    return (coffee_type or 'Coffee').replace('_', ' ').title()

def _fallback_journal_entries():
    return [
        {
            'id': 1,
            'title': 'Magic Latte',
            'cafe_name': 'Sideshow Espresso',
            'coffee_type': 'Latte',
            'rating': 5,
            'stars': '★★★★★',
            'photo_path': None,
            'notes': 'Incredibly silky texture with a sweet almond finish. Almost too pretty to drink.',
            'date_display': 'yesterday',
        },
        {
            'id': 2,
            'title': 'Single Origin Espresso',
            'cafe_name': 'Telegram Coffee',
            'coffee_type': 'Espresso',
            'rating': 4,
            'stars': '★★★★☆',
            'photo_path': None,
            'notes': 'Ethiopian Yirgacheffe - bright berry notes, clean chocolate finish.',
            'date_display': '3 days ago',
        },
        {
            'id': 3,
            'title': 'Cold Brew Tonic',
            'cafe_name': 'Humblebee',
            'coffee_type': 'Cold Brew',
            'rating': 4,
            'stars': '★★★★☆',
            'photo_path': None,
            'notes': 'Refreshing with tonic cutting through the bitterness. Great on a hot day.',
            'date_display': '5 days ago',
        },
        {
            'id': 4,
            'title': 'V60 Pour Over',
            'cafe_name': 'Strange Company',
            'coffee_type': 'Pour Over',
            'rating': 5,
            'stars': '★★★★★',
            'photo_path': None,
            'notes': 'Beautifully balanced. Floral jasmine notes with a honey sweetness.',
            'date_display': '1 week ago',
        },
    ]

def _journal_entry_from_log(log):
    coffee_type = _coffee_type_label(log.coffee_type)
    return {
        'id': log.id,
        'title': coffee_type,
        'cafe_name': log.cafe_name,
        'coffee_type': coffee_type,
        'rating': log.rating,
        'stars': _rating_stars(log.rating),
        'photo_path': log.photo_path,
        'notes': log.notes or 'No notes added yet.',
        'date_display': log.date_logged.strftime('%d %b %Y') if log.date_logged else 'No date',
    }

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
    using_fallback = False
    try:
        coffee_logs = CoffeeLog.query.order_by(CoffeeLog.date_logged.desc()).all()
        entries = [_journal_entry_from_log(log) for log in coffee_logs]
    except Exception:
        db.session.rollback()
        entries = _fallback_journal_entries()
        using_fallback = True

    return render_template('my_journal.html', entries=entries, using_fallback=using_fallback)

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
