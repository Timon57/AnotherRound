from django import forms
from .models import UserBase
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm,SetPasswordForm

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


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'Username','id':'login-user'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password','id':'login-pwd'}))

class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    username = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname', 'readonly': 'readonly'}))

    firstname = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))

    class Meta:
        model = UserBase
        fields = ('email', 'username', 'firstname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=255,widget=forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'Email','id':'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunately we can not find that email address'
            )
        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))

