from django.shortcuts import render, redirect
from django.urls import reverse

from . models import Couples

from .forms import CouplesRegistrtaion, CoupleUpdateForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def CouplesRegistration(request):
    if request.method == "POST":
        form = CouplesRegistrtaion(request.POST)

        if form.is_valid():

            couple_instance = form.save(commit=False)
            couple_instance.user = request.user
            couple_instance.save()

            messages.success(request, 'registred successfully!')
            return redirect('home')
        
    couple_exist = Couples.objects.filter(user=request.user).exists()

    if couple_exist:

        registred_copules = Couples.objects.get(user=request.user)
        groom_name = registred_copules.groomname # retrieing groom name 
        bride_name = registred_copules.bridename # retrieing bride name 
        context = {'registred_copules':registred_copules, 'groom_name':groom_name, 'bride_name':bride_name}
        return render(request, 'weeds/couples_exist.html', context)
    else:
        form = CouplesRegistrtaion()
        context = {"form":form} 
    return render(request, 'weeds/copuleregistration.html', context)

@login_required(login_url='login')
def coupleupdate(request, pk):
    couple = Couples.objects.get(id=pk)
    # form = CoupleUpdateForm(instance=couple)

    if request.method == "POST":
        form = CoupleUpdateForm(request.POST, instance=couple)
        if form.is_valid():
            form.save()
            # user = Couples.objects.get(user=request.user)
            # messages.success(request, f"{user} successfully updated Couples registration form!")
            # coupleview_url = reverse('CouplesRegistration', args=[couple.pk])
            return redirect('home')
    else:
        form = CoupleUpdateForm(instance=couple)
    context = {"form":form,'couple':couple}
    return render(request, 'weeds/couplesupdate.html', context)

@login_required(login_url='login')
def coupleview(request, pk):
    
    context = {}
    return render(request, 'weeds/couplesview', context)