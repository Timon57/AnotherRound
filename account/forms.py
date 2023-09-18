from django import forms
from .models import UserBase

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Enter Username',min_length=4,max_length=50,help_text='Required')
    email = forms.EmailField(max_length=100,help_text='Required',error_messages={'required':'please enter your email'})
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Pasword',widget=forms.PasswordInput)


    class Meta:
        model = UserBase
        fields = ('username','email')