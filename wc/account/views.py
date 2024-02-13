from django.shortcuts import render, redirect, reverse

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages

from .forms import (createUserForm, LoginForm, EditUserProfilrForm,
                    EditAdminProfilrForm, PasswordChangeForm)

from django.contrib.auth import (authenticate,
                                login as auth_login,
                                logout as auth_logout,
                                update_session_auth_hash,
                                )

from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required




from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model


from vender.models import Vendor

CustomUser = get_user_model()
# Create your views here.

# @login_required(login_url='login')
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
    if request.method == 'POST':

        form = createUserForm(request.POST,  request.FILES)

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
            # Form is invalid, so render the registration form template with form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = createUserForm()

    context = {'form':form}

    return render(request, 'acc/register.html', context)
           

@login_required(login_url='login')
def UserProfile(request, pk):

    user = CustomUser.objects.get(id=pk)

    context = {'user':user}
    
    return render(request, 'acc/user_profile.html', context)


@login_required(login_url='login')
def UpdateProfile(request, pk):
   
    user = CustomUser.objects.get(id=pk)
    # form = EditUserProfilrForm(instance = user)
    # form = EditAdminProfilrForm(instance = user)

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.is_superuser == True:
                form = EditAdminProfilrForm(request.POST, instance = user)
            else:
                form = EditUserProfilrForm(request.POST, request.FILES, instance = user)
            if form.is_valid():
                form.save()
                
                name = form.cleaned_data.get('name')
                messages.success(request, f"{name} updated Successfully!" )
                profile_url = reverse('user_profile', args=[user.pk])
                return redirect(profile_url)
        else:
            if request.user.is_superuser == True:
                form = EditAdminProfilrForm(instance=user)
            else:
                form = EditUserProfilrForm(instance=user)

        context={'form':form}
        return render(request, 'acc/update_profile.html', context)
        
    return render(request, 'acc/update_profile.html')

@login_required(login_url='login')
def ListUser(request):
    list_user = CustomUser.objects.all()
    list_vender = Vendor.objects.all()
    
    context = {'list_user':list_user, 'list_vender':list_vender}
    return render(request, 'acc/list_user.html', context)

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
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    messages.success(request,  f"Welcome, {email}! You've been logged in successfully." )

                    return redirect('home')
                
    context = {'form':form}


    return render(request, 'acc/login.html', context=context)

@login_required(login_url='login')
def Logout(request):

    auth_logout(request)

    messages.success(request, 'Sucessfully Logged out!')

    return redirect("home")


@login_required(login_url='login')
def ChangePassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Successfully Changed Password!")
            return redirect('home')
    
    else:

        form = PasswordChangeForm(user= request.user)
    context = {'form':form}
    return render(request, "acc/change-password.html", context)

