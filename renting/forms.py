from django import forms
from base.models import Booking
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.core.exceptions import ValidationError
from base.models import Booking, Equipment
from datetime import date

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['equipment', 'booking_date', 'return_date', 'amount']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'amount': 'กรุณากรอกจำนวนอุปกรณ์ที่ต้องการเช่า',
        }

    # การตรวจสอบความถูกต้องของวันที่แบบกำหนดเอง
    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        return_date = cleaned_data.get('return_date')
        amount = cleaned_data.get('amount')
        equipment = cleaned_data.get('equipment')

        # ตรวจสอบว่า return_date มากกว่า booking_date
        if booking_date and return_date:
            if return_date <= booking_date:
                raise ValidationError('วันที่คืนต้องมากกว่าวันที่จอง')

        # ตรวจสอบความพร้อมของอุปกรณ์
        if equipment and amount:
            if amount > equipment.available_amount:
                raise ValidationError(f'มีอุปกรณ์ {equipment.name} เหลือเพียง {equipment.available_amount} หน่วยเท่านั้น')

        return cleaned_data

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['equipment', 'return_date']
        widgets = {
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }