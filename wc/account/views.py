from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib import messages

from .forms import (createUserForm, LoginForm, )

from django.contrib.auth import authenticate, login as auth_login


# Create your views here.

def Home(request):
    return render(request, 'acc/index.html')
    
def Register(request):

    form = createUserForm()

    if request.method == 'POST':

        form = createUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Your Registration completed!')

            return redirect('home')

    context = {'form':form}

    return render(request, 'acc/register.html', context)



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

                messages.success(request, " ' "+ email +  " ' "+ '  Logged in successfully!' )

                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
                
                
          
    context = {'form':form}


    return render(request, 'acc/login.html', context=context)