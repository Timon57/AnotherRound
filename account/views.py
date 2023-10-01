from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .forms import RegistrationForm,UserEditForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .token import account_activation_token
from .models import UserBase
from orders.models import Order


def account_registration(request):
    if request.method == 'POST':
        registrationForm = RegistrationForm(request.POST)
        if registrationForm.is_valid():
            user = registrationForm.save(commit=False)
            user.email = registrationForm.cleaned_data['email']
            user.set_password(registrationForm.cleaned_data['password'])
            user.is_active = False
            user.save()

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
        registrationForm = RegistrationForm()
    return render(request,'account/registration/register.html',{'form':registrationForm})


def account_activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
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
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST,instance=request.user)

        if user_form.is_valid():
            user_form.save()
        else:
            print(user_form.errors)
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/user/edit_details.html', {'user_form': user_form})

@login_required
def delete_user(request):
    user = UserBase.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('delete-confirmation')


@login_required
def dashboard(request):
    return render(request,'account/user/dashboard.html')

def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)