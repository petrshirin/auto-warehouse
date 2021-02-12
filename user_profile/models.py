from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
import string
from random import choice


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fio = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=False)


class UserRegistrationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    is_used = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_student_additional_tables(sender: User, instance: User, created: bool, **kwargs):
    if created:
        text = f'Ваш код активации: {_generate_activation_code(instance)}'
        email = EmailMessage("Активируйте ваш аккаунт", text, to=[instance.email])
        email.send()


def _generate_activation_code(user: User) -> str:
    code = ''.join([choice(string.digits) for i in range(10)])
    UserRegistrationCode.objects.filter(user=user).update(is_used=True)
    UserRegistrationCode.objects.create(user=user, code=code)
    return code






