from constant import *


def get_student_or_teacher(user):
    user_extension = user.extension
    if hasattr(user_extension, "student"):
        return UserType.STUDENT, user_extension.student
    else:
        return UserType.TEACHER, user_extension.teacher