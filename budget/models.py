from django.conf import settings
from django.db import models

EXPENSE = 'expense'
INCOME = 'income'
TYPE_CHOICES = [
    (EXPENSE, 'هزینه'),
    (INCOME, 'درآمد'),
]


class Category(models.Model):
    name = models.CharField('نام دسته', max_length=100)
    type = models.CharField('نوع', max_length=10, choices=TYPE_CHOICES, default=EXPENSE)
    icon = models.CharField('آیکون', max_length=10, default='📁')

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return f'{self.icon} {self.name}'


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField('نوع', max_length=10, choices=TYPE_CHOICES, default=EXPENSE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='دسته')
    amount = models.PositiveBigIntegerField('مبلغ (تومان)')
    date = models.DateField('تاریخ')
    note = models.CharField('توضیحات', max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.get_type_display()} - {self.amount:,}'


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته')
    amount = models.PositiveBigIntegerField('سقف ماهانه (تومان)')

    class Meta:
        verbose_name = 'بودجه'
        verbose_name_plural = 'بودجه‌ها'
        constraints = [
            models.UniqueConstraint(fields=['user', 'category'], name='unique_budget_per_user_category'),
        ]

    def __str__(self):
        return f'{self.category.name} - {self.amount:,}'


class RecurringTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recurrings')
    type = models.CharField('نوع', max_length=10, choices=TYPE_CHOICES, default=EXPENSE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته')
    amount = models.PositiveBigIntegerField('مبلغ (تومان)')
    note = models.CharField('توضیحات', max_length=200, blank=True)
    start_date = models.DateField('تاریخ شروع')
    day_of_month = models.PositiveSmallIntegerField('روز ماه', default=1)
    active = models.BooleanField('فعال', default=True)
    last_generated = models.DateField('آخرین تولید', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تراکنش تکراری'
        verbose_name_plural = 'تراکنش‌های تکراری'
        ordering = ['active', '-created_at']

    def __str__(self):
        return f'{self.get_type_display()} {self.amount:,} هر ماه روز {self.day_of_month}'


class SavingsGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField('عنوان', max_length=100)
    icon = models.CharField('آیکون', max_length=10, default='🎯')
    target_amount = models.PositiveBigIntegerField('مبلغ هدف (تومان)')
    saved_amount = models.PositiveBigIntegerField('پس‌انداز شده (تومان)', default=0)
    target_date = models.DateField('تاریخ هدف', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'هدف پس‌انداز'
        verbose_name_plural = 'اهداف پس‌انداز'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
