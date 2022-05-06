import random
from faker import Faker
import sys
sys.path.append("..")
from app.models import *

nickname = Faker('zh_CN')
usrname = Faker()

def generate_organization():
    for oname in ['生活部', '艺术部', '外联部', '内联部', '学术部']:
        org = Organization.objects.create(oname=oname)
        org.save()

def generate_student():
    nickname = Faker('zh_CN')
    usrname = Faker()
    # with open("student_testcase.csv", 'w') as f:
    #     writer = csv.writer(f)
    for i in range(10):
        user = User.objects.create(username=usrname.name())
        user.set_password('1234')
        user.save()
        s = Student.objects.create(user=user, sname=nickname.name(), gender=random.randint(0,1))
        s.save()


def generate_teacher():
    nickname = Faker('zh_CN')
    usrname = Faker()
    for i in range(5):
        user = User.objects.create(username=usrname.name())
        user.set_password('1234')
        user.save()
        org = random.sample([i for i in Organization.objects.all()], 1)[0]
        t = Teacher.objects.create(user=user,
                                   tname=nickname.name(),
                                   gender=random.randint(0,1),
                                   organization=org)
        t.save()


def generate_all():
    generate_organization()
    generate_student()
    generate_teacher()
