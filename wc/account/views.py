from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib import messages

from .forms import (createUserForm, LoginForm, )

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.auth import get_user_model



from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from django.http import HttpResponse




CustomUser = get_user_model()
# Create your views here.

def Home(request):
    return render(request, 'acc/index.html')

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return redirect('acc_active_email_complete')
    else:  
        return redirect('acc_active_email_invalid')
       
    
def acc_active_email_complete(request):
    user = CustomUser.objects.all()
    context = {'user':user}
    return render(request, 'acc/acc_active_email_complete.html', context)
    

def acc_active_email_invalid(request):
    return render(request, 'acc/acc_active_email_invalid.html')


def Register(request):

    user = CustomUser.objects.all()

    form = createUserForm()

    if request.method == 'POST':

        form = createUserForm(request.POST)

        if form.is_valid():
            
            user = form.save(commit=False)

            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            mail_subject = 'Activation link has been sent to your email id'   
            message = render_to_string('acc/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            }) 
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )
            email.send()

            messages.success(request, f" {user.email} Please confirm your email address to complete the registration")
            
            return redirect('login')
        else:
            form = createUserForm()

            context = {'form':form, 'user':user}

            return render(request, 'acc/register.html', context)
            # for field, errors in form.errors.items():
            #     for error in errors:
            #         messages.error(request, f'{field.capitalize()}: {error}')



    return render(request, 'acc/register.html')


def Login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data = request.POST) 

        if form.is_valid():

            # 'username' corresponds to the email field in AuthenticationForm
            email = request.POST.get('username') 
            password = request.POST.get('password')

            user = authenticate(request, username=email,  password=password)

            if user is not None:
                
                auth_login(request, user)

                messages.success(request,  f"Welcome, {email}! You've been logged in successfully." )

                return redirect('home')
                
    context = {'form':form}


    return render(request, 'acc/login.html', context=context)


def Logout(request):

    auth_logout(request)

    messages.success(request, 'Sucessfully Logged out!')

    return redirect("home")


