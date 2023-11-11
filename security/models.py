from django.db import models
from django.contrib.auth.models import AbstractUser

from learn_htmx.mixins import TimeStampMixin


# Create your models here.

class User(AbstractUser, TimeStampMixin):
    city = models.CharField(max_length=128, null=True, blank=True)
    # stake_address = models.CharField(max_length=255, null=True, blank=True, unique=True)
    # word_key = models.CharField(max_length=255, null=True, blank=True, unique=True)

    def __str__(self):
        return self.email
    
