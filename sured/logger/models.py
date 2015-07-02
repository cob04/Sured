from ..models import db

class AccountCreation(db.Model):
    __tablename__ = 'account_creations'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer)

class PostCreation(db.Model):
    __tablename__ = 'post_creations'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
