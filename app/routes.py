<<<<<<< HEAD
from flask import flash, redirect, render_template, url_for, request
=======
from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
>>>>>>> origin/main
from app import app, db
from app.forms import CoffeeLogForm
import os
from app.models import CoffeeLog, Message, User
from flask_login import current_user, login_required


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
            'coffee_type_value': 'latte',
            'rating': 5,
            'stars': '★★★★★',
            'photo_path': None,
            'notes': 'Sample entry',
            'date_display': 'yesterday',
<<<<<<< HEAD
        }
=======
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
>>>>>>> origin/main
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

<<<<<<< HEAD

# ---------------- ROUTES ---------------- #

@app.route('/')
=======
def _entry_count():
    return CoffeeLog.query.filter_by(user_id=current_user.id).count()

@app.route('/', methods=['GET', 'POST'])
>>>>>>> origin/main
def home():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/my_journal')
def my_journal():
    using_fallback = False
    try:
        coffee_logs = CoffeeLog.query.filter_by(user_id=current_user.id).order_by(CoffeeLog.date_logged.desc()).all()
        entries = [_journal_entry_from_log(log) for log in coffee_logs]
        entry_count = len(entries)
    except Exception:
        db.session.rollback()
        entries = _fallback_journal_entries()
        entry_count = len(entries)
        using_fallback = True

<<<<<<< HEAD
    return render_template('my_journal.html', entries=entries, using_fallback=using_fallback)
=======
    return render_template('my_journal.html', entries=entries, entry_count=entry_count, using_fallback=using_fallback)

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

    return jsonify({'success': True, 'entry_count': _entry_count()})
>>>>>>> origin/main


@app.route('/log-coffee', methods=['GET', 'POST'])
def log_coffee():
    form = CoffeeLogForm()

    if form.validate_on_submit():
        photo = form.photo.data
        filename = photo.filename

        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        entry = CoffeeLog(
            cafe_name=form.cafe_name.data,
            coffee_type=form.coffee_type.data,
            rating=form.rating.data,
            photo_path=f'uploads/{filename}',
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
<<<<<<< HEAD


# 🔥 UPDATED EXPLORE (DATABASE USERS)
@app.route('/explore')
def explore():
    users = User.query.all()
    return render_template('Explore.html', users=users)


@app.route('/user/<int:id>')
def user(id):
    return render_template('user.html')


# ---------------- MESSAGING ---------------- #

# 🔥 Redirect /messages → first available chat
@app.route('/messages')
@login_required
def messages_redirect():
    first_user = User.query.filter(User.id != current_user.id).first()

    if not first_user:
        return "No users available to chat"

    return redirect(url_for('chat', user_id=first_user.id))


# 🔥 Open chat with specific user
@app.route('/messages/<int:user_id>')
@login_required
def chat(user_id):
    other_user = User.query.get(user_id)
    users = User.query.filter(User.id != current_user.id).all()

    return render_template(
        'messages.html',
        user=other_user,
        users=users
    )


# 🔥 Send message
@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    receiver_id = request.form.get('receiver_id')
    content = request.form.get('content')

    if not content:
        return {'status': 'error'}

    msg = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content
    )

    db.session.add(msg)
    db.session.commit()

    return {'status': 'ok'}


# 🔥 Get messages between users
@app.route('/get_messages/<int:user_id>')
@login_required
def get_messages(user_id):
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp).all()

    return [{
        'sender': m.sender_id,
        'content': m.content
    } for m in messages]
=======
>>>>>>> origin/main
