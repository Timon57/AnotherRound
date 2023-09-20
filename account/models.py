from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,PermissionsMixin)
from django.utils.translation import gettext_lazy as _ 
from django.core.mail import send_mail


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)
    
    def create_user(self,email,username,password,**other_fields):
        if not email:
            raise ValueError(_('you must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user

class UserBase(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=100,blank=True)
    email = models.EmailField(_('email address'),unique=True)
    phone_number = models.CharField(max_length=10,blank=True)
    address = models.CharField(max_length=250,blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )


    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.username



    
