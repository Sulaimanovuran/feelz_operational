from .service import AddStudentDB

def create_success_message_for_tg(student_data: AddStudentDB):
    message = f'Студент *{student_data.student.name}* успешно записан\n \
               \t\t*Расписание:*\n```\n'
    
    for num, day in enumerate(student_data.days):
        message+=f'\n{num+1}. {day}'

    message+="\n```"

    return message

    
