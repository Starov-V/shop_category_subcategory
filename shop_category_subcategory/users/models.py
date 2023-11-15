from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    password = models.CharField(
        max_length=150,
        null=True,
        default=None,
    )
    email = models.EmailField(
        unique=True,
        max_length=254
    )