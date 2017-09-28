#!/usr/bin/env python3

"""Documentation about the module... may be multi-line"""

from django.utils.translation import ugettext_lazy as _
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
    letters = string.ascii_letters + string.digits + string.ascii_lowercase
    return ''.join(SystemRandom().choice(letters) for _ in range(length))


class PublicProfile(models.Model):

    user        = models.OneToOneField(User, related_name='public_profile')
    public_info = models.TextField()
    identifier  = models.CharField(max_length=15, default=make_identifier, blank=True)
    auth        = models.CharField(max_length=15, default=make_identifier, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['identifier', 'auth']),
        ]


class Case(models.Model):

    TYPE_CHOICES = (
        ('no_damage', _('No Damage')),
        ('property_damage', _('Property Damage')),
        ('injury', _('Injury')),
    )

    damage_type  = models.CharField(max_length=20, choices=TYPE_CHOICES, default='no_damage')

    model_owner    = models.ForeignKey(User, related_name='cases')
    identifier     = models.CharField(max_length=10, default=make_identifier, blank=True)
    timestamp      = models.DateTimeField(auto_now_add=True)

    reporter_email = models.EmailField()

    class Meta:
        indexes = [
            models.Index(fields=['identifier']),
        ]


class CaseMessage(models.Model):

    case       = models.ForeignKey(Case, related_name = 'messages')
    timestamp  = models.DateTimeField(auto_now_add=True)
    from_owner = models.BooleanField()
    message    = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
        ]

