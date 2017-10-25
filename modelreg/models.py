#!/usr/bin/env python3

"""Documentation about the module... may be multi-line"""

from django.utils.translation import ugettext_lazy as _
from random import SystemRandom
from datetime import timedelta
from django.utils import timezone
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
    identifier     = models.CharField(max_length=15, default=make_identifier, blank=True)
    timestamp      = models.DateTimeField(auto_now_add=True)

    owner_resolved  = models.BooleanField(default=False)
    finder_resolved = models.BooleanField(default=False)
    admin_informed  = models.BooleanField(default=False)

    reporter_email = models.EmailField()

    class Meta:
        indexes = [
            models.Index(fields=['identifier']),
        ]

    def can_escalate(self, mode):
        """Return True if escalation towards admins is possible.

        The current rule is that you can escalate if the other party
        has been quiet for over 5 days, OR there has been at least
        some communication from the other side.

        Accepts a mode, which represents the current user's role
        in this case: 'owner', or 'finder'. Any other value is rejected
        """
        assert mode in ('finder', 'owner')

        look_for = {
            'finder': 'owner',
            'owner': 'finder'
        }[mode]

        newest_from_other = (self.messages
                             .filter(sender=look_for)
                             .order_by('-timestamp'))

        if not newest_from_other.exists():
            # The other party never wrote!
            # Return True if case is older than our delta
            days_ago = timezone.now() - timedelta(days=5)
            return self.timestamp > days_ago

        # Other party did write at least once. Since we don't know
        # why the user may be escalating, let's allow it.
        return True

    @property
    def can_owner_escalate(self):
        return self.can_escalate('owner')

    @property
    def can_finder_escalate(self):
        return self.can_escalate('finder')


class CaseMessage(models.Model):

    SENDER_CHOICES=(
        ('admin', _('Administrator')),
        ('finder', _('Finder')),
        ('owner', _('Owner')),
    )

    case       = models.ForeignKey(Case, related_name = 'messages')
    timestamp  = models.DateTimeField(auto_now_add=True)
    for_admin  = models.BooleanField(default=False)
    message    = models.TextField()

    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)

    @property
    def from_owner(self):
        return self.sender == 'owner'


    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
        ]

