import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


def removes_migrations():
    base_dir = settings.BASE_DIR
    exclude = {'__init__.py'}
    for root, dirs, filenames in os.walk(base_dir):
        if root.endswith("migrations"):
            for filename in set(filenames) - exclude:
                os.remove(os.path.join(root, filename))


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('reset_db', '--noinput')
        removes_migrations()
        call_command('makemigrations')
        call_command('migrate')
