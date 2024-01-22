from django.contrib.auth.models import AbstractUser
from django.db import models
from Exp.models import Areas

class CustomUsers(AbstractUser):
    area = models.ForeignKey(Areas, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.username

