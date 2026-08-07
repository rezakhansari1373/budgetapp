from datetime import date

import jdatetime

from .models import Transaction

RECURRING_FREQUENCY = 'monthly'


def days_in_jmonth(jyear, jmonth):
    first = jdatetime.date(jyear, jmonth, 1)
    if jmonth == 12:
        next_first = jdatetime.date(jyear + 1, 1, 1)
    else:
        next_first = jdatetime.date(jyear, jmonth + 1, 1)
    return (next_first.togregorian() - first.togregorian()).days


def generate_recurring_transactions(user, up_to=None):
    if up_to is None:
        up_to = date.today()
    created = 0
    for rec in user.recurrings.filter(active=True).select_related('category'):
        start = rec.start_date
        if start > up_to:
            continue
        cursor = jdatetime.date.fromgregorian(date=start)
        last_gen = rec.last_generated
        while True:
            jyear, jmonth = cursor.year, cursor.month
            occ_day = min(rec.day_of_month, days_in_jmonth(jyear, jmonth))
            occ = jdatetime.date(jyear, jmonth, occ_day).togregorian()
            if occ >= start and occ <= up_to and (last_gen is None or occ > last_gen):
                Transaction.objects.create(
                    user=user, type=rec.type, category=rec.category,
                    amount=rec.amount, date=occ, note=rec.note,
                )
                created += 1
                last_gen = occ
            if jmonth == 12:
                cursor = jdatetime.date(jyear + 1, 1, 1)
            else:
                cursor = jdatetime.date(jyear, jmonth + 1, 1)
            if cursor.togregorian() > up_to:
                break
        if last_gen and last_gen != rec.last_generated:
            rec.last_generated = last_gen
            rec.save(update_fields=['last_generated'])
    return created
