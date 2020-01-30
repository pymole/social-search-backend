from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=False)
    email = models.EmailField('email address', unique=True)
    vk_token = models.CharField(max_length=256, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{}".format(self.email)

    @property
    def is_vk_authorized(self):
        return bool(self.vk_token)
