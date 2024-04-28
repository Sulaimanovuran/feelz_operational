import gspread

#Подключение к таблице Google Sheets
sa = gspread.service_account()
sh = sa.open_by_url("https://docs.google.com/spreadsheets/d/1hE0xs25iBil169bLxH8jvIimvUgOKruQojNg5lXGfhI/edit?usp=sharing")


class GoogleSheets:
    """Класс для создания записи в Google Таблице"""

    def __init__(self, student_data):
        self.student = student_data
        self.worksheets = {"mwf": "even", "tts": "odd", "ed": "every_day", 
                           "mwf_pay": "Payment_even", "tts_pay": "Payment_odd", "ed_pay": "Payment_every_day"}

    def write_student(self):
        try:
            # Открываем нужный лист и получаем данные
            wks = sh.worksheet(self.worksheets[self.student.subscription.ads])
            writed_data = wks.get("A3:BZ500")
            
            # Добавляем наши данные в общий список и записываем
            writed_data.append([self.student.student.name] + self.student.days)
            wks.update("A3:BZ500", writed_data)
            
        except gspread.exceptions.APIError as ex:
            print(ex)
            return f"ERROR: Ошибка записи в таблицу {self.worksheets[self.student.subscription.ads]}"
        except Exception as ex:
            return f"ERROR: {ex}"
        
        return f"SUCCESS: Студент {self.student.student.name} успешно записан"

