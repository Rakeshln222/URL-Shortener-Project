from flask_sqlalchemy import SQLAlchemy
import string
import random
from datetime import datetime

db = SQLAlchemy()

class ShortenedURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clicks = db.Column(db.Integer, default=0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_code = self.generate_short_code()
    
    def generate_short_code(self):
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choices(characters, k=6))
            # Ensure the code is unique
            if not ShortenedURL.query.filter_by(short_code=short_code).first():
                return short_code
    
    def __repr__(self):
        return f'<ShortenedURL {self.original_url} -> {self.short_code}>'