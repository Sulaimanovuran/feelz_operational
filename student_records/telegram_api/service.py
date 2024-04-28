from ..database import Student, Subscription, Payment, Day, db
from datetime import datetime


def home():
    return {"Hello":"world"}



class AddStudentDB:
    """Класс для создания студента в БД,
       вместе со связанными объектами: Абонемент: Subscription, Оплата: Payment, Даты занятий: Days"""

    def __init__(self, student_name: str, subscription_type: str, days: str) -> None:
        self.student: Student = self.add_student(student_name)
        self.subscription: Subscription = self.add_subscription(subscription_type)
        self.payment: Payment = self.add_payment()
        self.days: list[str] = days

        
    def add_student(self, student_name):
        student = Student(name=student_name)
        db.session.add(student)
        db.session.commit()
        
        return student


    def add_subscription(self, subscription_type='mwf'):
        subscription = Subscription(student_id=self.student.id, ads=subscription_type)
        db.session.add(subscription)
        db.session.commit()
        return subscription


    def add_payment(self):
        payment = Payment(student_id=self.student.id, amount=5000,
                    month=datetime.now().strftime('%Y-%m'),
                    subscriptions_added=1)
        db.session.add(payment)
        db.session.commit()
        return payment
    
    
    def add_days(self, days):
        new_days = []
        for date_str in days:
            try:
                date = datetime.strptime(date_str, "%d.%m.%Y")
                day = Day(student_id=self.student.id, lesson_date=date, subscription_id=self.subscription.id)
                db.session.add(day)
                new_days.append(date_str)
            except ValueError as ex:
                print(ex)
                return "ERROR: Некоректный формат даты"
            except Exception as ex:
                return f"ERROR: Ошибка добавления данных {ex}"
        db.session.commit()
        return new_days

