from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create our own DBUser based on django.contrib.auth.models.User
# According to https://docs.djangoproject.com/zh-hans/4.0/topics/auth/customizing/#extending-the-existing-user-models
class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')
    # Add new user field Here
    # ...


@receiver(post_save, sender=User)
def create_user_extension(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)
    else:
        instance.extension.save()