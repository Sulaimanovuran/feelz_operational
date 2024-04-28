from flask import Blueprint, request, jsonify
from datetime import datetime

from ..database import db, Day
from .service import home, AddStudentDB
from .utils import create_success_message_for_tg
from student_records.google_sheets.services import GoogleSheets


tg = Blueprint('main', __name__, url_prefix='/api')


@tg.route('/')
def index():
    return home()


@tg.route("/add", methods=["POST"])
def post():

    message = ''
    data = request.get_json()
    student_name = data.get('name')
    subscription_type = data.get('subscription_type')
    days = data.get('days')

    # Создание данных об ученике его абонементе, оплате и дат занятий
    try:
        student_data = AddStudentDB(student_name=student_name, subscription_type=subscription_type, days=days)
    except Exception as ex:
        message=f"Ошибка добавления данных в БД:\n{ex}" 

    gs = GoogleSheets(student_data=student_data)
    gs_record = gs.write_student()
    message=gs_record

    if "SUCCESS" in gs_record:
        return jsonify({"message": create_success_message_for_tg(student_data)}), 201
    else:
        return jsonify({"message": message}), 500