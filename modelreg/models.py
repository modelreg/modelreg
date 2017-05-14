#!/usr/bin/env python3

"""Documentation about the module... may be multi-line"""

from random import SystemRandom
import string
import json
import base64
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    user  = models.OneToOneField(User, related_name='profile')

    address = models.TextField()
    phone   = models.CharField(max_length=50)


def make_identifier(length=15):
    letters = string.ascii_letters + string.digits
    return ''.join(SystemRandom().choice(letters) for _ in range(length))


class PublicProfile(models.Model):

    user        = models.OneToOneField(User, related_name='public_profile')
    public_info = models.TextField()
    identifier  = models.CharField(max_length=10, default=make_identifier)
    auth        = models.CharField(max_length=10, default=make_identifier)

    class Meta:
        indexes = [
            models.Index(fields=['identifier', 'auth']),
        ]
