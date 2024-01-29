from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from Exp.models import Areas


class CustomUsers(AbstractUser):
    area = models.ForeignKey(Areas, on_delete=models.SET_NULL, blank=False, null=True)

    def save(self, *args, **kwargs):
        # Cifrar la contraseña antes de guardar el usuario
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

