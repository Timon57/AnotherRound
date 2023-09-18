from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from .forms import RegistrationForm
from .token import account_activation_token

def account_registration(request):
    print('############################')
    if request.method == 'POST':
        registrationForm = RegistrationForm(request.POST)
        print('***********************')
        print(registrationForm)
        if registrationForm.is_valid():
            user = registrationForm.save(commit=False)
            user.email = registrationForm.cleaned_data['email']
            user.set_password(registrationForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            print('------------')
            print(user)
            #setting up email
            current_site = get_current_site(request)
            subject = 'Activate you Account'
            message = render_to_string('account/registration/account_activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(bytes(str(user.pk))),
                'token':account_activation_token.make_token(user),
            })
            user.email_user(subject=subject,message=message)
            return HttpResponse('Registration successful! Check your email to activate your account')
    else:
        print('-------hello------')
        registrationForm = RegistrationForm()
    return render(request,'account/registration/register.html',{'form':registrationForm})