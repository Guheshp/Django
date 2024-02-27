from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages

from django.conf import settings
from django.core.mail import send_mail

from .forms import (createUserForm,CreateUserVenderForm, LoginForm, EditUserProfilrForm, EditAdminProfilrForm, PasswordChangeForm, ContactForm)

from django.contrib.auth import (authenticate,
                                login as auth_login,
                                logout as auth_logout,
                                update_session_auth_hash,
                                )

from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required

# gmail 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model

from . decorators import unauthenticated_user, allowed_users, admin_only

from django.contrib.auth.models import Group

from .models import Contact

from vender.models import Vendor,ServiceDetails

CustomUser = get_user_model()
# Create your views here.

# @login_required(login_url='login')
# @unauthenticated_user
# @allowed_users(allowed_roles=['admin','vendor','customer'])
@admin_only
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

# registrationchoice------------------

def registrationchoice(request):
    if request.method == 'POST':

        selected_option = request.POST.get('registration_option')
        if selected_option == 'register_user':
            return redirect('register')  # Redirect to the user registration page
        elif selected_option == 'register_vendor':
            return redirect('VendorRegister')  # Redirect to the vendor registration page
    return render(request,'acc/registerationchoice.html')

@unauthenticated_user
def Register(request):
    if request.method == 'POST':
        form = createUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            is_customer = form.cleaned_data.get('is_customer', False)
            user.is_active = False
            user.save()

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            if is_customer:
                group = Group.objects.get(name="customer")
                user.groups.add(group)

                # Send activation email
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string('acc/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

                messages.success(request, f"{user.email} You have been registered as User, Please check your email to activate your account.")
            else:
                messages.error(request, "Something went wrong while registration!")

            return redirect('login')
        else:
            # Form is invalid, so render the registration form template with form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = createUserForm()
    context = {'form': form}
    return render(request, 'acc/register.html', context)         


@unauthenticated_user
def VendorRegister(request):
    if request.method == 'POST':
        form = CreateUserVenderForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            is_vendor = form.cleaned_data.get('is_vendor', False)
            user.is_active = False
            user.save()

            # Assign user to vendor group
            group = Group.objects.get(name='vendor')
            user.groups.add(group)

            if is_vendor:
                group = Group.objects.get(name="vendor")
                user.groups.add(group)

                # Send activation email
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string('acc/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

                messages.success(request, f"{user.email} You have been registered as a vendor, Please check your email to activate your account.")
            else:
                messages.error(request, "Something went wrong while registration ")

            return redirect('login')
        else:
            # Form is invalid, so render the registration form template with form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = CreateUserVenderForm()
    context = {'form': form}
    return render(request, 'acc/vendor_register.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','vendor','customer'])
def UserProfile(request, pk):

    user = CustomUser.objects.get(id=pk)

    context = {'user':user}
    
    return render(request, 'acc/user_profile.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','vendor','customer'])
def UpdateProfile(request, pk):
   
    user = get_object_or_404(CustomUser, id=pk)
    # form = EditUserProfilrForm(instance = user)
    # form = EditAdminProfilrForm(instance = user)
    if request.method == 'POST':
            if request.user.is_superuser == True:
                form = EditAdminProfilrForm(request.POST, instance=user)
            else:
                form = EditUserProfilrForm(request.POST, request.FILES, instance=user)
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
        


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def ListUser(request):
    list_user = CustomUser.objects.all()
    list_vender = Vendor.objects.all()
    context = {'list_user':list_user, 'list_vender':list_vender}
    return render(request, 'acc/list_user.html', context)

@allowed_users(allowed_roles=['admin'])
def querieslist(request):
    querieslist = Contact.objects.all()
    context = {'querieslist':querieslist}
    return render(request, 'acc/querieslist.html', context)


@unauthenticated_user
def Login(request):
    form = LoginForm()
    if request.method == "POST":

        form = LoginForm(request, data=request.POST) 

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
@allowed_users(allowed_roles=['admin','vendor','customer'])
def Logout(request):

    auth_logout(request)

    messages.success(request, 'Sucessfully Logged out!')

    return redirect("home")


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','vendor','customer'])
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

# contact us page 
def contactview(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            user_email = form.cleaned_data['user_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Construct the email subject
            email_subject = f'New contact {user_email}: {subject}'

            # Load the email message template and render it with the form data
            email_message = render_to_string('acc/contact_email_template.html', {
                'user_email': user_email,
                'subject': subject,
                'message': message,
            })

            email = EmailMessage(
                subject=email_subject,
                body=email_message,
                from_email=settings.EMAIL_FROM,
                to=settings.ADMIN_EMAILS,
                reply_to=[user_email]  # Set the Reply-To header
            )
            email.send(fail_silently=False)

            #reply to contact form email 
            user_email_subject = 'Thank you for contacting us'

            user_email_message = render_to_string('acc/contact_user_email_template.html', {
                'user_email': user_email,
            })

            user_email = EmailMessage(
                subject=user_email_subject,
                body=user_email_message,
                from_email=settings.EMAIL_FROM,
                to=[user_email],
            )
            user_email.send(fail_silently=False)

            # Save the form data to the database
            form.save()
            useremail = form.cleaned_data.get('user_email')
            messages.success(request, f'{useremail} Thank you for contacting us!')
            return redirect('contactview')

    else:
        form=ContactForm()
    
    context = {'form':form}
    return render(request, 'acc/contact.html', context)



# if admin logged he will be directed to this page 
@login_required(login_url='login')
def admin(request):

    return render(request, 'acc/admin.html')

# if registered as vender he will be directed to this page 
@login_required(login_url='login')
def newvendor(request):
    vendor = Vendor.objects.all()
    context = {"vendor":vendor}
    return render(request, 'acc/venderpage.html', context)

@login_required(login_url='login')
def myservices(request):
    vendor = Vendor.objects.all()

    context = {"vendor":vendor}
    return render(request, 'acc/myservices.html', context)

def addDetails(request):
    vendor = Vendor.objects.all()
    context={"vendor":vendor}
    return render(request, 'acc/addDetails.html', context)

# vender services view
@login_required(login_url='login')
def vendorservice(request, pk):
    vendor = Vendor.objects.get(id=pk)
    #retriveung all servives respective vendor
    services = vendor.services.all()
    servicesdetails = ServiceDetails.objects.filter(vendor=vendor, service__in=services)


    context = {'vendor':vendor,"services":services, 'servicesdetails':servicesdetails}
    return render(request, 'acc/vendorservice.html', context)

# if registered as newcustomer he will be directed to this page 
def newcustomer(request):
    return render(request, 'acc/customerpage.html')
