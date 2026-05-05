from app import db
from datetime import datetime, timezone

class CoffeeLog(db.Model):
    __tablename__ = 'coffee_log'
    
    id = db.Column(db.Integer, primary_key=True) #PK for each entry
    cafe_name = db.Column(db.String(100), nullable=False)
    coffee_type = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    photo_path = db.Column(db.String(200), nullable=True)  # stores file path, not the image
    notes = db.Column(db.Text, nullable=True)
    date_logged = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) #stores the date and time when the entry was created
    user_id = db.Column(db.Integer, nullable=True)  # placeholder for when User table is added with the login system

    def __repr__(self):
        return f'<CoffeeLog {self.id} - {self.cafe_name} - {self.coffee_type}>'