from ..database import Student, Subscription, Payment, db
from datetime import datetime


def home():
    return {"Hello":"world"}


def add_student(name):
    obj = Student(name=name)
    db.session.add(obj)
    db.session.commit()
    return obj


def add_subscription(student_id, ads):
    subscription = Subscription(student_id=student_id, ads=ads)
    db.session.add(subscription)
    db.session.commit()
    return subscription


def add_payment(student_id):
    obj = Payment(student_id=student_id, amount=5000,
                  month=datetime.now().strftime('%Y-%m'),
                  subscriptions_added=1)

    db.session.add(obj)
    db.session.commit()
    return obj
