from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('reset_db_migrations')
        call_command('generate_superuser')
        call_command('loaddata', 'provinces.json', 'regencies.json')
