from flask import Blueprint, request, jsonify
from ..database import db, Day
from .service import home, add_student, add_subscription, add_payment
from datetime import datetime


tg = Blueprint('main', __name__, url_prefix='/api')


@tg.route('/')
def index():
    return home()


@tg.route("/add", methods=["POST"])
def post():
    data = request.get_json()
    student_name = data.get('student_name')
    subscription_type = data.get('subscription_type')
    days = data.get('days')

    # Создаем объект студента
    student = add_student(student_name)

    # Создаем объект подписки
    subscription = add_subscription(student_id=student.id, ads=subscription_type)

    # Создаем объекты посещений для каждой даты
    for date_str in days:
        date = datetime.strptime(date_str, "%d.%m.%Y")
        day = Day(student_id=student.id, lesson_date=date, subscription_id=subscription.id)
        db.session.add(day)

    # Создаем объект платежа
    add_payment(student_id=student.id)

    return jsonify({"message": "Студент успешно создан"}), 201