from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class URLShortenerResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    long_url = models.TextField()
    short_url = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True, db_index=True)