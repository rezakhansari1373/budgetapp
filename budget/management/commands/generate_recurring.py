from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from budget.services import generate_recurring_transactions


class Command(BaseCommand):
    help = 'ایجاد تراکنش‌های تکراری موعد گذشته برای همه کاربران'

    def handle(self, *args, **options):
        total = 0
        for user in User.objects.all():
            total += generate_recurring_transactions(user)
        self.stdout.write(f'{total} recurring transaction(s) created.')
