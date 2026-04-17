from database.db import db

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    result = db.Column(db.Text)
    user_id = db.Column(db.Integer)
