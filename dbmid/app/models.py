from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create our own DBUser based on django.contrib.auth.models.User
# According to https://docs.djangoproject.com/zh-hans/4.0/topics/auth/customizing/#extending-the-existing-user-models
class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')
    name = models.CharField("姓名", max_length=10, null=True)

    class Gender(models.IntegerChoices):
        MALE = (0, "男")
        FEMALE = (1, "女")

    gender = models.SmallIntegerField(
        "性别", choices=Gender.choices, null=True, blank=True
    )


class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True)


class Student(UserExtension):
    student_id = models.AutoField(primary_key=True)


class Teacher(UserExtension):
    teacher_id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)  # Organization that the teacher belongs to


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    poster = models.ForeignKey(Student, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Organization, on_delete=models.CASCADE)  # Organization that receives the post
    title = models.CharField("标题", max_length=30, blank=False)
    content = models.TextField("内容", blank=False)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)    # Post that the comment belongs to
    content = models.TextField("内容", blank=False)


@receiver(post_save, sender=User)
def create_user_extension(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)
    else:
        instance.extension.save()
