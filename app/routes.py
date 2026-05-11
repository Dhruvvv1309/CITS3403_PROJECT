from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import CoffeeLogForm, LoginForm, SignupForm
import os
from app.models import CoffeeLog, User

def _user_initials(username):
    parts = (username or 'User').split()
    if len(parts) >= 2:
        return ''.join(part[0] for part in parts[:2]).upper()
    return parts[0][:2].upper()

def _rating_stars(rating):
    rating = int(rating or 0)
    rating = max(0, min(rating, 5))
    return '★' * rating + '☆' * (5 - rating)

def _coffee_type_label(coffee_type):
    return (coffee_type or 'Coffee').replace('_', ' ').title()

def _favorite_coffee_badge(logs):
    if not logs:
        return 'No regular yet'

    counts = {}
    for log in logs:
        counts[log.coffee_type] = counts.get(log.coffee_type, 0) + 1

    favorite = max(counts, key=counts.get)
    return f'{_coffee_type_label(favorite)} regular'

def _activity_badge(entry_count):
    if entry_count == 0:
        return 'New Sipper'
    if entry_count < 5:
        return 'Starter'
    if entry_count < 20:
        return 'Explorer'
    return 'Coffee Pro'

def _fallback_journal_entries():
    return [
        {
            'id': 1,
            'title': 'Magic Latte',
            'cafe_name': 'Sideshow Espresso',
            'coffee_type': 'Latte',
            'coffee_type_value': 'latte',
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
            'coffee_type_value': 'espresso',
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
            'coffee_type_value': 'cold_brew',
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
            'coffee_type_value': 'pour_over',
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
        'coffee_type_value': log.coffee_type,
        'rating': log.rating,
        'stars': _rating_stars(log.rating),
        'photo_path': log.photo_path,
        'notes': log.notes or 'No notes added yet.',
        'date_display': log.date_logged.strftime('%d %b %Y') if log.date_logged else 'No date',
    }

def _entry_count():
    return CoffeeLog.query.filter_by(user_id=current_user.id).count()

def _current_user_logs():
    return CoffeeLog.query.filter_by(user_id=current_user.id).order_by(CoffeeLog.date_logged.desc()).all()

@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('my_journal'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in.')
            return redirect(url_for('home'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('my_journal'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/explore')
@login_required
def explore():
    return render_template('Explore.html')

@app.route('/my_journal')
@login_required
def my_journal():
    using_fallback = False
    try:
        coffee_logs = _current_user_logs()
        entries = [_journal_entry_from_log(log) for log in coffee_logs]
        entry_count = len(entries)
        favorite_badge = _favorite_coffee_badge(coffee_logs)
    except Exception:
        db.session.rollback()
        entries = _fallback_journal_entries()
        entry_count = len(entries)
        favorite_badge = _favorite_coffee_badge([])
        using_fallback = True

    return render_template(
        'my_journal.html',
        activity_badge=_activity_badge(entry_count),
        entries=entries,
        entry_count=entry_count,
        favorite_badge=favorite_badge,
        user_initials=_user_initials(current_user.username),
        using_fallback=using_fallback,
    )

@app.route('/my_journal/<int:entry_id>/edit', methods=['POST'])
@login_required
def edit_journal_entry(entry_id):
    entry = CoffeeLog.query.filter_by(id=entry_id, user_id=current_user.id).first()
    if entry is None:
        return jsonify({'success': False, 'error': 'Entry not found.'}), 404

    data = request.get_json() or {}
    cafe_name = (data.get('cafe_name') or '').strip()
    coffee_type = (data.get('coffee_type') or '').strip()

    try:
        rating = int(data.get('rating', entry.rating))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'error': 'Rating must be a number.'}), 400

    if not cafe_name or not coffee_type or rating < 1 or rating > 5:
        return jsonify({'success': False, 'error': 'Please enter a cafe, coffee type, and rating from 1 to 5.'}), 400

    entry.cafe_name = cafe_name
    entry.coffee_type = coffee_type
    entry.rating = rating
    entry.notes = data.get('notes', entry.notes)
    db.session.commit()

    return jsonify({'success': True, 'entry': _journal_entry_from_log(entry)})

@app.route('/my_journal/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_journal_entry(entry_id):
    entry = CoffeeLog.query.filter_by(id=entry_id, user_id=current_user.id).first()
    if entry is None:
        return jsonify({'success': False, 'error': 'Entry not found.'}), 404

    db.session.delete(entry)
    db.session.commit()
    entry_count = _entry_count()

    return jsonify({'success': True, 'activity_badge': _activity_badge(entry_count), 'entry_count': entry_count})

@app.route('/log-coffee', methods=['GET', 'POST'])
@login_required
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
            notes=form.notes.data,
            user_id=current_user.id)
        db.session.add(entry)
        db.session.commit()
        flash('Coffee logged successfully!')
        return redirect(url_for('my_journal'))
    return render_template('log-coffee.html', title='Log a Coffee', form=form)

@app.route('/game')
def game():
    return render_template('game.html')
