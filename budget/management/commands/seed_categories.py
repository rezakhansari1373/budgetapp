from django.core.management.base import BaseCommand

from budget.models import Category

DEFAULT_CATEGORIES = [
    ('expense', 'خوراک', '🍔'),
    ('expense', 'مسکن', '🏠'),
    ('expense', 'حمل‌ونقل', '🚌'),
    ('expense', 'تفریح', '🎮'),
    ('expense', 'پوشاک', '👕'),
    ('expense', 'بهداشت', '🩺'),
    ('expense', 'تحصیل', '📚'),
    ('expense', 'سایر هزینه‌ها', '📦'),
    ('income', 'حقوق', '💼'),
    ('income', 'فریلنسر', '💻'),
    ('income', 'سایر درآمدها', '💵'),
]


class Command(BaseCommand):
    help = 'ایجاد دسته‌بندی‌های پیش‌فرض'

    def handle(self, *args, **options):
        created = 0
        for ttype, name, icon in DEFAULT_CATEGORIES:
            obj, was_created = Category.objects.get_or_create(name=name, type=ttype, defaults={'icon': icon})
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created} default categories.'))
