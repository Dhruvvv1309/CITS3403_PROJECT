from app import db, login_manager
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# ---------------- LOGIN LOADER ---------------- #

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# ---------------- COFFEE LOG ---------------- #

class CoffeeLog(db.Model):
    __tablename__ = 'coffee_log'
    
    id = db.Column(db.Integer, primary_key=True)
    cafe_name = db.Column(db.String(100), nullable=False)
    coffee_type = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    photo_path = db.Column(db.String(200))
    notes = db.Column(db.Text)
    date_logged = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<CoffeeLog {self.cafe_name} - {self.coffee_type}>"


# ---------------- USER ---------------- #

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Optional feature (used in matching)
    favourite_coffee = db.Column(db.String(50))

    date_joined = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    coffee_logs = db.relationship('CoffeeLog', backref='user', lazy=True)

    sent_messages = db.relationship(
        'Message',
        foreign_keys='Message.sender_id',
        backref='sender',
        lazy=True
    )

    received_messages = db.relationship(
        'Message',
        foreign_keys='Message.receiver_id',
        backref='receiver',
        lazy=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


# ---------------- MESSAGE ---------------- #

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    content = db.Column(db.Text, nullable=False)

    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Message {self.id} from {self.sender_id} to {self.receiver_id}>"