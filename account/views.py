from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from .forms import RegistrationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .token import account_activation_token
from .models import UserBase

def account_registration(request):
    if request.method == 'POST':
        registrationForm = RegistrationForm(request.POST)
        if registrationForm.is_valid():
            user = registrationForm.save(commit=False)
            user.email = registrationForm.cleaned_data['email']
            user.set_password(registrationForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            print(user)
            #setting up email
            current_site = get_current_site(request)
            subject = 'Activate you Account'
            message = render_to_string('account/registration/account_activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            user.email_user(subject=subject,message=message)
            return HttpResponse('Registration successful! Check your email to activate your account')
    else:
        print('-------hello------')
        registrationForm = RegistrationForm()
    return render(request,'account/registration/register.html',{'form':registrationForm})


def account_activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_encode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect('dashboard')
    else:
        return render(request,'account/registration/activation_invalid.html')


@login_required
def dashboard(request):
    return render(request,'account/dashboard.html')