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

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        u = UserBase.objects.filter(username=username)
        if u.count():
            raise forms.ValidationError('Username already exists')
        return username
    
    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return data['password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        u = UserBase.objects.filter(email=email)
        if u.count():
            raise forms.ValidationError('Email already exists, Please use another email')
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})
