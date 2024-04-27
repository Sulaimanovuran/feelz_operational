from os.path import abspath, dirname
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

BASE_DIR = dirname(dirname(abspath(__file__)))

DB_URL = "sqlite:///" + BASE_DIR + "/db.feelz_students"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subscriptions = db.relationship('Subscription', backref='student', lazy=True)
    payments = db.relationship('Payment', backref='student', lazy=True)
    days = db.relationship('Day', backref='student', lazy=True)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # Пн•Ср•Пт, Вт•Чт•Сб, Каждый день
    lessons_remaining = db.Column(db.Integer, default=0)
    days = db.relationship('Day', backref='subscription', lazy=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(7), nullable=False)  # Формат: YYYY-MM
    subscriptions_added = db.Column(db.Integer, nullable=False)

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    lesson_date = db.Column(db.Date, nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)