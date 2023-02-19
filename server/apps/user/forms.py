from django import forms
from .models import Profile
from django.contrib.auth.models import User
from datetime import datetime

class DateInput(forms.DateInput):
  input_type = 'date'

class ProfileUpdateForm(forms.ModelForm):
  # birth_date = forms.DateField()
  # birth_date.widget.attrs.update({'placeholder': "yyyy-mm-dd"})
  
  class Meta:
    model = Profile
    fields = ['profile_image', 'phone_num', 'height', 'weight', 'gender', 'birth_date']
    widgets = {'birth_date':DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'required': 'required'})}
    
class DateUpdateForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['birth_date']
    widgets = {'birth_date':DateInput(attrs={'type':'date', 'placeholder': 'YYYY-MM-DD', 'required': 'required'})}