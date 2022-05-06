from site import USER_BASE
from app.constant import *

def get_student_or_teacher(user):
    user_extension = user.extension
    if hasattr(user_extension, "student"):
        return UserType.STUDENT, user_extension.student
    else:
        return UserType.TEACHER, user_extension.teacher

def get_bardisplay(
    navbar_name,
    user_type="student",
    warn_code=None,
    warn_message=None,

):
    bar_display = {
        "navbar_name": navbar_name,
        "user_type": user_type,    
    }
    if warn_code:
        bar_display['warn_code'] = warn_code
        bar_display['warn_message'] = warn_message
    return bar_display
    
def get_user_nickname(user):
    type_, obj_ = get_student_or_teacher(user)
    if type_ == UserType.TEACHER:
        return obj_.tname
    else:
        return obj_.sname