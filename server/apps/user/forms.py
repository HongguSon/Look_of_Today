from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
  birth_date = forms.DateField()
  birth_date.widget.attrs.update({'placeholder': "yyyy-mm-dd"})
  
  class Meta:
    model = Profile
    fields = ['profile_image', 'phone_num', 'height', 'weight', 'age', 'birth_date']