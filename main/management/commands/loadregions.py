from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from main.models import Province, Regency
from region.utils import PROVINCES, REGENCIES

User = get_user_model()


class Command(BaseCommand):
    help = ("Load region data from csv files to database.")

    def handle(self, *args, **options):
        # Id for province in sumatera island harcoded from region files
        ids = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '21']

        for id in ids:
            Province.objects.get_or_create(name=PROVINCES[id])

        for province in Province.objects.all():
            code = {v: k for k, v in PROVINCES.items()}[province.name]
            regencies = []
            for id, name in REGENCIES.items():
                if id[:2] == code:
                    regencies.append(name)
            for name in regencies:
                Regency.objects.get_or_create(
                    province=province,
                    name=name,
                )
