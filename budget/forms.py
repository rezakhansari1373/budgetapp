import jdatetime
from django import forms

from .models import TYPE_CHOICES, Transaction, Category

FA_TO_EN = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')


class TransactionForm(forms.ModelForm):
    date = forms.CharField(
        label='تاریخ (شمسی)',
        widget=forms.TextInput(attrs={
            'placeholder': 'مثلاً ۱۴۰۵/۰۵/۱۶',
            'inputmode': 'numeric',
            'dir': 'ltr',
        }),
    )

    class Meta:
        model = Transaction
        fields = ['type', 'category', 'amount', 'date', 'note']
        widgets = {
            'type': forms.RadioSelect(choices=TYPE_CHOICES),
            'category': forms.Select(),
            'amount': forms.NumberInput(attrs={'placeholder': 'مثلاً ۵۰۰۰۰۰', 'min': 1}),
            'note': forms.TextInput(attrs={'placeholder': 'مثلاً: خرید نان', 'maxlength': 200}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].label = 'نوع تراکنش'
        self.fields['amount'].label = 'مبلغ (تومان)'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['type'].widget.attrs['class'] = 'radio-group'
        if self.instance and self.instance.date:
            self.fields['date'].initial = jdatetime.date.fromgregorian(date=self.instance.date).strftime('%Y/%m/%d')
        else:
            self.fields['date'].initial = jdatetime.date.today().strftime('%Y/%m/%d')

    def clean_date(self):
        raw = self.cleaned_data['date']
        text = str(raw).strip().translate(FA_TO_EN).replace('-', '/')
        parts = text.split('/')
        if len(parts) != 3:
            raise forms.ValidationError('تاریخ را به فرمت شمسی وارد کنید، مثلاً: ۱۴۰۵/۰۵/۱۶')
        try:
            y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
            return jdatetime.date(y, m, d).togregorian()
        except (ValueError, TypeError):
            raise forms.ValidationError('تاریخ واردشده نامعتبر است.')
