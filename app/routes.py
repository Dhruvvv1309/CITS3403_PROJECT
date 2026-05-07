from flask import flash, redirect, render_template, url_for
from app import app, db
from app.forms import CoffeeLogForm
import os
from app.models import CoffeeLog


# ---------------- HELPER FUNCTIONS ---------------- #

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
            'notes': 'Incredibly silky texture with a sweet almond finish.',
            'date_display': 'yesterday',
        }
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


# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return render_template('login.html')


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
        photo = form.photo.data
        photo_filename = photo.filename
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        photo_path = f'uploads/{photo_filename}'

        entry = CoffeeLog(
            cafe_name=form.cafe_name.data,
            coffee_type=form.coffee_type.data,
            rating=form.rating.data,
            photo_path=photo_path,
            notes=form.notes.data
        )

        db.session.add(entry)
        db.session.commit()

        flash('Coffee logged successfully!')
        return redirect(url_for('my_journal'))

    return render_template('log-coffee.html', form=form)


@app.route('/game')
def game():
    return render_template('game.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/user/<int:id>')
def user(id):
    return render_template('user.html')