from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Vendor
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import VenderRegistrationForm, VenderUpdateForm

# Create your views here.

login_required(login_url='login')
def venderRegistration(request):
    form = VenderRegistrationForm()

    if request.method == "POST":
        form = VenderRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(request, "vender registration form created")

            return redirect("home")

    context={"form":form}
    return render(request, 'vender/registration.html', context)

login_required(login_url='login')
def VenderUpdate(request, pk):

    vender = Vendor.objects.get(id=pk)
    form = VenderUpdateForm(instance=vender)

    if request.method == "POST":
        form = VenderUpdateForm(request.POST, request.FILES, instance=vender)

        if form.is_valid():
            form.save()

            vender_name = form.cleaned_data.get('vender_name')
            messages.success(request, f"{vender_name} form updated!")

            venderview_url = reverse('venderview', args=[vender.pk])

            return redirect(venderview_url)
    
    context={'form':form, 'vender':vender}
        
    return render(request, 'vender/updatevender.html', context)


login_required(login_url='login')
def venderViewAll(request):

    vender = Vendor.objects.all().order_by('-id')

    context={"venders":vender}

    return render(request, 'vender/viewvender_registration.html', context)

login_required(login_url='login')
def deleteVender(request, pk):
    vender = Vendor.objects.get(id=pk)

    if request.method == "POST":

        vender.delete()
        messages.success(request, 'vender deleted successfully!')
        return redirect("venderviewall")
    
    context = {"vender":vender}
    return render(request, 'vender/delete_vender.html', context)

login_required(login_url='login')
def vebderView(request, pk):
    vender = Vendor.objects.get(id=pk)

    context = {"vender":vender}
    return render(request, 'vender/venderview.html', context)

