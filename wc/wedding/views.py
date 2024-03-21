from django.shortcuts import render, redirect
from django.urls import reverse

from . models import Couples

from .forms import CouplesRegistrtaion, CoupleUpdateForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

from datetime import date

CustomUser = get_user_model()

# Create your views here.
@login_required(login_url='login')
def CouplesRegistration(request):
    if request.method == "POST":
        form = CouplesRegistrtaion(request.POST)

        if form.is_valid():

            groom_dob = form.cleaned_data.get('groom_dob')
            bride_dob = form.cleaned_data.get('bride_dob')

            groom_age = (date.today() - groom_dob).days // 365
            bride_age = (date.today() - bride_dob).days // 365

            if groom_age < 21:
                form.add_error('groom_dob', 'Groom must be at least 21 years old.')
            if bride_age < 21:
                form.add_error('bride_dob', 'Bride must be at least 21 years old.')

            if not form.errors:
                couple_instance = form.save(commit=False)
                couple_instance.user = request.user
                couple_instance.save()

                messages.success(request, 'registred successfully!')
                return redirect('home')
    else:

        form = CouplesRegistrtaion()
        
    couple_exist = Couples.objects.filter(user=request.user).exists()

    if couple_exist:

        registered_couples = Couples.objects.get(user=request.user)
        groom_name = registered_couples.groomname # retrieing groom name 
        bride_name = registered_couples.bridename # retrieing bride name 
        
        groom_dob = registered_couples.groom_dob
        bride_dob = registered_couples.bride_dob

        groom_age = (date.today() - groom_dob).days // 365
        bride_age = (date.today() - bride_dob).days // 365

       

        context = {'registered_couples':registered_couples,
                    'groom_name':groom_name,
                    'bride_name':bride_name,
                    'groom_age':groom_age,
                    'bride_age':bride_age,
                }
        return render(request, 'weeds/couples_exist.html', context)
    else:
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
            groomname = form.cleaned_data.get('groomname')
            bridename = form.cleaned_data.get('bridename')

            messages.success(request, f' {groomname} & {bridename} updated  successfully!')
            return redirect('CouplesRegistration')

    else:
        form = CoupleUpdateForm(instance=couple)
    context = {"form":form,'couple':couple}
    return render(request, 'weeds/couplesupdate.html', context)

@login_required(login_url='login')
def coupleall(request):
    couple = Couples.objects.all().order_by('-id')
    context = {'couple':couple}
    return render(request, 'weeds/coupleall.html', context)

def coupleview(request, pk):
    couple = Couples.objects.get(id=pk)
    context = {'couple':couple}
    return render(request, 'weeds/coupleview.html', context)


def coupledelete(request, pk):
    couple = Couples.objects.get(id=pk)

    if request.method == "POST":

        couple.delete()
        messages.success(request, 'couples deleted successfully!')
        # return redirect("couplesall")
        coupleall_url = reverse('venderview', args=[couple.pk])
        return redirect(coupleall)
    
    context = {"couple":couple}
    return render(request, 'weeds/delete_couple.html', context)