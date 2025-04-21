from app import db
from datetime import datetime

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    publication_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Book {self.title}>"