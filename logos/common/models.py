from django.db import models
from django.contrib.auth.models import AbstractUser	# AbstractUser 불러오기

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    joindate = models.DateTimeField(blank=True, null=True)
    admin_yn = models.CharField(max_length=1, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=2, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    