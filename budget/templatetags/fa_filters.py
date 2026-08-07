from django import template
import jdatetime

register = template.Library()

PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹'
TRANSLATION_TABLE = str.maketrans('0123456789', PERSIAN_DIGITS)

MONTH_NAMES = ['', 'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
               'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']


@register.filter
def pnum(value):
    return str(value).translate(TRANSLATION_TABLE)


@register.filter
def jdate(value, fmt='%Y/%m/%d'):
    if not value:
        return ''
    try:
        return jdatetime.date.fromgregorian(date=value).strftime(fmt).translate(TRANSLATION_TABLE)
    except (TypeError, ValueError):
        return ''


@register.filter
def divshare(value, total):
    try:
        total = int(total)
        if total <= 0:
            return '۰'
        return f'{int(value) / total * 100:.0f}'.translate(TRANSLATION_TABLE)
    except (TypeError, ValueError, ZeroDivisionError):
        return '۰'


@register.filter
def pmoney(value):
    try:
        grouped = f'{int(value):,}'.translate(TRANSLATION_TABLE)
        return grouped.replace(',', '٬')
    except (TypeError, ValueError):
        return '۰'


@register.filter
def pmonth(value):
    try:
        return MONTH_NAMES[int(value)]
    except (TypeError, ValueError, IndexError):
        return value
