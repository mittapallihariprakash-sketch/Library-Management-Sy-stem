import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        username = os.environ.get("DJANGO_ADMIN_USER")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not username or not password:
            self.stdout.write("Admin credentials are not configured.")
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, "", password)
            self.stdout.write("Admin user created successfully.")
        else:
            self.stdout.write("Admin user already exists.")