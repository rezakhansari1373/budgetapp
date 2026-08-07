import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'ساخت کاربر ادمین از متغیرهای محیطی ADMIN_USERNAME/ADMIN_EMAIL/ADMIN_PASSWORD'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', '').strip()
        email = os.environ.get('ADMIN_EMAIL', '').strip()
        password = os.environ.get('ADMIN_PASSWORD', '').strip()

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                'ADMIN_USERNAME/ADMIN_PASSWORD تنظیم نشده‌اند؛ کاربر ادمین ساخته نشد.'
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'Admin "{username}" already exists.'))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Admin "{username}" created.'))
