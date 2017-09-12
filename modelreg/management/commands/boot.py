#!/usr/bin/env python3

import os

from django.core.management.base import BaseCommand
from django.core.management import call_command

from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Boot the modelreg application'


    def handle(self, *args, **options):
        if 'SUPERUSER_NAME' in os.environ:
            self.create_superuser()
        if os.getenv('MIGRATE', 'false').lower() == 'true':
            self.migrate()

        self.run_app()

    def create_superuser(self):
        user = User()
        user.is_superuser = True
        user.is_staff     = True

        user.username = os.getenv('SUPERUSER_NAME')
        user.email    = os.getenv('SUPERUSER_EMAIL')
        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.save()
        print("Superuser created: %s" % user.username)

    def migrate(self):
        call_command('migrate')

    def run_app(self):
        call_command('runserver', os.getenv('ADDRPORT', 'localhost:8080'))
