#!/usr/bin/env python3

"""Documentation about the module... may be multi-line"""

import json
import base64
from django.db import models
from django.contrib.auth.models import User


class EncdataMixin(models.Model):

    # data_encrypted shall only be decrypted via a key derived at login time,
    # preferrably from the password, or even better - a QR code as well.
    # Optionally, we could provide a PIN. At this moment, encryption is not
    # implemented, so it's simply a base64 json dump.
    data_encrypted = models.TextField()

    def get_data(self, passkey):
        return json.load(base64.b64decode(self.data_encrypted))

    def set_data(self, passkey, data):
        self.data_encrypted = base64.b64encode(json.dumps(data))

    class Meta:
        abstract = True


class Profile(EncdataMixin):

    user  = models.OneToOneField(User)


class PublicProfile(EncdataMixin):

    profile = models.ForeignKey(Profile, related_name='public_profiles')
