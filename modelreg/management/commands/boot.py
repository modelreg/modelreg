#!/usr/bin/env python3

import os

import time

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db.utils import ProgrammingError

from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Boot the modelreg application'


    def handle(self, *args, **options):
        if self.has_flag('COLLECTSTATIC'):
            self.collectstatic()

        if self.has_flag('MIGRATE'):
            self.migrate()

        if 'SUPERUSER_NAME' in os.environ:
            self.create_superuser()

        self.run_app()

    def create_superuser(self):
        user, created = User.objects.get_or_create(
            username = os.getenv('SUPERUSER_NAME'),
            email    = os.getenv('SUPERUSER_EMAIL')
        )
        user.is_superuser = True
        user.is_staff     = True

        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.save()
        action = {True: 'created', False: 'updated'}[created]

        print("Superuser %s: %s" % (action, user.username))

    def migrate(self):
        # We may need to wait for the DB to become available
        self._wait_for_db()
        print("Migrating DB...")
        call_command('migrate')

    def run_app(self):
        port = os.getenv('PORT', '9090')
        host = '0.0.0.0'

        from django.conf import settings

        if self.has_flag('UWSGI'):
            os.execvp(
                'uwsgi',
                ['--http',
                 ':%d' % port,
                 '--wsgi-file',
                 os.path.join(settings.BASE_DIR, 'modelreg', 'wsgi.py')]
            )
        else:
            call_command('runserver', '%s:%s'  %(host, port))

    def collectstatic(self):
        call_command('collectstatic', '--noinput')

    def _wait_for_db(self):
        for _ in range(15):
            try:
                _ = User.objects.first()
            except ProgrammingError:
                # Not a connection error anymore, so DB is ready
                return
            except Exception as exc:
                print("Waiting for DB...")
                time.sleep(1)

    def has_flag(self, flag):
        print("Checking for env flag %s: %s" % (flag, os.getenv(flag, 'false')))
        return os.getenv(flag, 'false').lower() == 'true'
