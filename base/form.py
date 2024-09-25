from django import forms

from base.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForms(UserCreationForm):
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=20, required=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'contact_number', 'password1', 'password2']
    
    def save(self , commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.contact_number = self.cleaned_data['contact_number']
        user.role = 'Student'
        if commit:
            user.save()
        return user
