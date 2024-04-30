import gspread
from ..database import Student, Subscription
from student_records.telegram_api.service import AddStudentDB

# Подключение к таблице Google Sheets
sa = gspread.service_account()
sh = sa.open_by_url("https://docs.google.com/spreadsheets/d/1hE0xs25iBil169bLxH8jvIimvUgOKruQojNg5lXGfhI/edit?usp=sharing")


class GoogleSheets:
    """Класс для создания записи в Google Таблице"""

    def __init__(self, student_data: AddStudentDB):
        self.student = student_data
        self.worksheets = {"mwf": "even", "tts": "odd", "ed": "every_day", 
                           "mwf_pay": "Payment_even", "tts_pay": "Payment_odd", "ed_pay": "Payment_every_day"}

    def write_student_with_payment(self):
        try:

            # Формируем данные для записи с учетом нового студента
            student_payment_rows = []
            student_lessons_rows = []
            try:
                # Получаем всех студентов для нужного типа абонемента
                students = Student.query.join(Subscription).filter(Subscription.ads == self.student.subscription.ads).order_by(Student.name).all()
                
                for student in students:
                    # Получаем все абонементы студента
                    subscriptions = student.subscriptions
                    student_lessons_row = [student.name]
                    student_payment_row = [student.name]

                    for subscription in subscriptions:
                        if subscription.is_paid:
                            student_payment_row.append("Оплачено")
                        else:
                            student_payment_row.append("Не оплачено")

                        # Получаем даты занятий для текущего абонемента и добавляем их в список student_lessons_row
                        student_lessons_row+=[day.lesson_date.strftime("%d.%m.%Y") for day in subscription.days]

                    # Добавляем списки данных об оплате и датах занятий в соответствующие итоговые списки
                    student_payment_rows.append(student_payment_row)
                    student_lessons_rows.append(student_lessons_row)

            except Exception as ex:
                print(ex)
                return f"ERROR: Ошибка чтения Базы данных {ex}"
            
            # Открываем нужные листы и записываем данные
            wks = sh.worksheet(self.worksheets[self.student.subscription.ads])
            wks.batch_clear(["A3:BZ500"])
            wks.update("A3:BZ500", student_lessons_rows)

            wks_pay = sh.worksheet(self.worksheets[f"{self.student.subscription.ads}_pay"])
            wks_pay.batch_clear(["A3:BZ500"])
            wks_pay.update("A3:BZ500", student_payment_rows)



        except gspread.exceptions.APIError as ex:
            print(ex)
            return f"ERROR: Ошибка записи в таблицу {self.worksheets[self.student.subscription.ads]}"
        except Exception as ex:
            return f"ERROR: {ex}"
        
        return f"SUCCESS: Студент {self.student.student.name} успешно записан"

