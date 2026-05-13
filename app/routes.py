from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import CoffeeLogForm, LoginForm, SignupForm
import os
from app.models import CoffeeLog, User
from app.models import Message
from sqlalchemy import or_, and_


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



# ── Explore (now passes real DB users) ──────────────────────

@app.route('/explore')
@login_required
def explore():                          # replaces the stub above
    users = User.query.all()
    return render_template('Explore.html', users=users)


# ── Messages page ────────────────────────────────────────────

@app.route('/messages')
@app.route('/messages/<int:other_id>')
@login_required
def messages(other_id=None):
    """
    Render the messages page.
    If other_id is given, that conversation is pre-selected via JS.
    Pass all other users so the sidebar can be populated.
    """
    users = User.query.filter(User.id != current_user.id).all()

    # Build conversation list: for each user this person has chatted with,
    # grab the latest message and unread count.
    conversations = []
    for u in users:
        latest = (
            Message.query
            .filter(
                or_(
                    and_(Message.sender_id == current_user.id, Message.receiver_id == u.id),
                    and_(Message.sender_id == u.id,            Message.receiver_id == current_user.id),
                )
            )
            .order_by(Message.timestamp.desc())
            .first()
        )
        unread = (
            Message.query
            .filter_by(sender_id=u.id, receiver_id=current_user.id, read=False)
            .count()
        )
        if latest:
            conversations.append({
                'user':    u,
                'preview': latest.body[:60],
                'time':    latest.timestamp.strftime('%H:%M'),
                'unread':  unread,
            })

    # Sort by most recent first; users with no messages go to the bottom
    conversations.sort(key=lambda c: c['time'], reverse=True)

    # Users with no messages yet (so they still show up in New Message modal)
    talked_ids = {c['user'].id for c in conversations}
    fresh_users = [u for u in users if u.id not in talked_ids]

    return render_template(
        'messages.html',
        conversations=conversations,
        fresh_users=fresh_users,
        open_user_id=other_id,
    )


# ── API: fetch messages between current user and another ─────

@app.route('/api/messages/<int:other_id>')
@login_required
def api_get_messages(other_id):
    other = User.query.get_or_404(other_id)

    # Mark messages from the other person as read
    Message.query.filter_by(
        sender_id=other_id,
        receiver_id=current_user.id,
        read=False
    ).update({'read': True})
    db.session.commit()

    msgs = (
        Message.query
        .filter(
            or_(
                and_(Message.sender_id == current_user.id, Message.receiver_id == other_id),
                and_(Message.sender_id == other_id,        Message.receiver_id == current_user.id),
            )
        )
        .order_by(Message.timestamp.asc())
        .all()
    )

    return jsonify({
        'other': {'id': other.id, 'username': other.username},
        'messages': [m.to_dict() for m in msgs],
    })


# ── API: send a message ───────────────────────────────────────

@app.route('/api/messages/<int:other_id>/send', methods=['POST'])
@login_required
def api_send_message(other_id):
    other = User.query.get_or_404(other_id)
    data  = request.get_json() or {}
    body  = (data.get('body') or '').strip()

    if not body:
        return jsonify({'success': False, 'error': 'Message cannot be empty.'}), 400

    msg = Message(sender_id=current_user.id, receiver_id=other_id, body=body)
    db.session.add(msg)
    db.session.commit()

    return jsonify({'success': True, 'message': msg.to_dict()})


# ── API: unread count (for nav badge) ────────────────────────

@app.route('/api/messages/unread')
@login_required
def api_unread_count():
    count = Message.query.filter_by(receiver_id=current_user.id, read=False).count()
    return jsonify({'unread': count})

# ── API: Find a match based on shared coffee logs ────────────
# Append this to the bottom of your existing routes.py

# ── REPLACE the existing /api/match route in routes.py with this ──────────

@app.route('/api/match')
@login_required
def api_match():
    """
    Match users by:
      - coffee_type (from dropdown, optional)
      - cafe_name   (free text, optional, partial match)
    At least one must be provided OR we fall back to scanning all logs.
    """
    coffee_filter = (request.args.get('coffee_type') or '').strip().lower()
    cafe_filter   = (request.args.get('cafe_name')   or '').strip().lower()

    # If nothing provided, use the current user's own logs to find matches
    use_user_logs = not coffee_filter and not cafe_filter

    if use_user_logs:
        my_logs = CoffeeLog.query.filter_by(user_id=current_user.id).all()
        if not my_logs:
            return jsonify({
                'success': False,
                'message': "Log some coffees first and we'll find your matches! ☕"
            })
        my_coffees = {log.coffee_type.lower().strip() for log in my_logs if log.coffee_type}
        my_cafes   = {log.cafe_name.lower().strip()   for log in my_logs if log.cafe_name}
    else:
        my_coffees = {coffee_filter} if coffee_filter else set()
        my_cafes   = {cafe_filter}   if cafe_filter   else set()

    other_users = User.query.filter(User.id != current_user.id).all()

    scored = []
    for user in other_users:
        their_logs = CoffeeLog.query.filter_by(user_id=user.id).all()
        if not their_logs:
            continue

        their_coffees = {log.coffee_type.lower().strip() for log in their_logs if log.coffee_type}
        their_cafes   = {log.cafe_name.lower().strip()   for log in their_logs if log.cafe_name}

        # Coffee: exact match
        shared_coffees = my_coffees & their_coffees

        # Cafe: partial match (user typed "telegram" matches "Telegram Coffee")
        shared_cafes = set()
        for my_cafe in my_cafes:
            for their_cafe in their_cafes:
                if my_cafe in their_cafe or their_cafe in my_cafe:
                    shared_cafes.add(their_cafe)

        # Must match at least one of the filters if filters were provided
        if not use_user_logs:
            coffee_ok = (not coffee_filter) or bool(shared_coffees)
            cafe_ok   = (not cafe_filter)   or bool(shared_cafes)
            if not (coffee_ok and cafe_ok):
                continue

        score = len(shared_coffees) * 2 + len(shared_cafes)
        if score == 0:
            continue

        reasons = []
        if shared_coffees:
            reasons.append(f"both love {', '.join(c.title() for c in shared_coffees)}")
        if shared_cafes:
            reasons.append(f"both visit {', '.join(c.title() for c in shared_cafes)}")

        scored.append({
            'id':             user.id,
            'username':       user.username,
            'score':          score,
            'reason':         " and ".join(reasons),
            'shared_coffees': list(shared_coffees),
            'shared_cafes':   list(shared_cafes),
        })

    if not scored:
        msg = "No matches found"
        if coffee_filter and cafe_filter:
            msg = f"No one shares {coffee_filter.title()} at {cafe_filter.title()} yet!"
        elif coffee_filter:
            msg = f"No one else has logged {coffee_filter.title()} yet!"
        elif cafe_filter:
            msg = f"No one else has visited '{cafe_filter.title()}' yet!"
        else:
            msg = "No matches yet — invite friends to join cuplog! ☕"
        return jsonify({'success': False, 'message': msg})

    scored.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'success': True, 'matches': scored[:3]})