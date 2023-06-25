# bluus/management/commands/createsu.py

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from decouple import config

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='bluu_admin').exists():
            User.objects.create_superuser(
                username='bluu_admin',
                password=config('ADMIN_PASSWORD')
            )
        print('Superuser has been created.')