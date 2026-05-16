from app import db, login_manager
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class CoffeeLog(db.Model):
    __tablename__ = 'coffee_log'
    
    id = db.Column(db.Integer, primary_key=True)
    cafe_name = db.Column(db.String(100), nullable=False)
    coffee_type = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    photo_path = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    date_logged = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_coffee_log_user'), nullable=True)

    def __repr__(self):
        return f'<CoffeeLog {self.id} - {self.cafe_name} - {self.coffee_type}>'

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    date_joined = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    coffee_logs = db.relationship('CoffeeLog', backref='user', lazy=True, foreign_keys='CoffeeLog.user_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>' 



class Message(db.Model):
    __tablename__ = 'message'
 
    id          = db.Column(db.Integer, primary_key=True)
    sender_id   = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_msg_sender'),   nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_msg_receiver'), nullable=False)
    body        = db.Column(db.Text, nullable=False)
    timestamp   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    read        = db.Column(db.Boolean, default=False)
 
    sender   = db.relationship('User', foreign_keys=[sender_id],   backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
 
    def to_dict(self):
        return {
            'id':          self.id,
            'sender_id':   self.sender_id,
            'receiver_id': self.receiver_id,
            'body':        self.body,
            'timestamp':   self.timestamp.strftime('%H:%M'),
            'date':        self.timestamp.strftime('%d %b %Y'),
            'read':        self.read,
        }
 
    def __repr__(self):
        return f'<Message {self.id}: {self.sender_id} → {self.receiver_id}>'
