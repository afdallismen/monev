from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    help = ("Create a superuser account, "
            "with username and password as 'admin'.")

    def handle(self, *args, **options):
        admin, ign = User.objects.get_or_create(
            username="admin",
            is_superuser=True,
        )
        admin.set_password("admin")
        admin.is_staff = True
        admin.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully created {!s}".format(admin))
        )
