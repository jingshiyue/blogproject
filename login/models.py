from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class Userprofile(AbstractUser):	#AbstractUser自带username、password、email、first_name、last_name
    gender = (
        ('male', '男'),
        ('female', '女')
    )
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)
    birthday = models.DateField("出生年月",null=True, blank=True)
    mobile = models.CharField("电话", max_length=11,default=12356)
    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('Userprofile', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'
