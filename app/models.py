from app import db
from datetime import datetime

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.String(2048))
    category = db.Column(db.String(128))
    image = db.Column(db.String(128))  # filename of feature image
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Article {}>'.format(self.title)