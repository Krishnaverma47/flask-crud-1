import datetime
from app import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    employees = db.relationship('Employee', backref='admin', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    def __init__(self, name, email, admin_id):
        self.name = name
        self.email = email
        self.admin_id = admin_id 
