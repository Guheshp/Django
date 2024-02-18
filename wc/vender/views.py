from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Vendor, Service, ReviewVender
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from account.decorators import unauthenticated_user, allowed_users, admin_only

from django.contrib.auth.decorators import login_required

from .forms import VenderRegistrationForm, VenderUpdateForm, ReviewForm
# Create your views here.

@login_required(login_url='login')
@admin_only
def venderRegistration(request,):

    form = VenderRegistrationForm()

    if request.method == "POST":
        form = VenderRegistrationForm(request.POST, request.FILES)

        if form.is_valid():

            vender = form.save(commit=False)
            vender.user = request.user
            vender.save()
            # Save the services associated with the vendor
            form.save_m2m()
            messages.success(request, "vender registration form created")

            return redirect("home")
        
    vendor_exists = Vendor.objects.filter(user=request.user).exists()
    
    if vendor_exists:

        # Get the name of the registered vendor

        registered_vendor = Vendor.objects.get(user=request.user)
        service = registered_vendor.services.all()

        # messages.success(request,'allready registred')

        context = {"registered_vendor": registered_vendor, 
                    "service":service, }

        return render(request, 'vendor/vender_exists.html', context)

    else:
        context={"form":form}
    return render(request, 'vendor/registration.html', context)


@login_required(login_url='login')
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
    else:
        form = VenderUpdateForm(instance=vender)
    context = {'form': form, 'vender': vender}
    return render(request, 'vendor/updatevender.html', context)



@login_required(login_url='login')
def venderViewAll(request):

    vender = Vendor.objects.all().order_by('-id')

    context={"venders":vender}

    return render(request, 'vendor/viewvender_registration.html', context)

@login_required(login_url='login')
def deleteVender(request, pk):
    vender = Vendor.objects.get(id=pk)

    if request.method == "POST":

        vender.delete()
        messages.success(request, 'vendor deleted successfully!')
        return redirect("venderviewall")
    
    context = {"vender":vender}
    return render(request, 'vendor/delete_vender.html', context)

@login_required(login_url='login')
def vebderView(request, pk):
    vender = Vendor.objects.get(id=pk)
    service = vender.services.all()
    context = {"vender":vender, 'service':service}
    return render(request, 'vendor/venderview.html', context)

login_required(login_url='login')
def services(request):
    return render(request, 'vendor/services.html')

# caterview and their details -----------------------------------------

login_required(login_url='login')
def catering(request):
    cater_vendors = Vendor.objects.filter(services__service_name='Catering')
    context = {'cater':cater_vendors, }
    return render(request, 'vendor/catering.html', context)

login_required(login_url='login')
def caterView(request, pk):

    vender = get_object_or_404(Vendor, pk=pk)
    service = vender.services.all()

    review = ReviewVender.objects.filter(vendor=vender).order_by('-created_at')

    context = {"vender":vender,'service':service,'review':review}

    return render(request, 'vendor/cater_details.html', context)

# decorview and their details -----------------------------------------

login_required(login_url='login')
def decor(request):

    decor_vendors = Vendor.objects.filter(services__service_name='Decor')
    context = {'decor':decor_vendors}
                
    return render(request, 'vendor/decor.html', context)


login_required(login_url='login')
def decorView(request, pk):

    vender = get_object_or_404(Vendor, pk=pk)
    service = vender.services.all()

 # getting all review
    review = ReviewVender.objects.filter(vendor=vender).order_by('-created_at')

    context = {"vender":vender, 'service':service, 'review':review}

    return render(request, 'vendor/decor_details.html', context)

# planningview and their details -----------------------------------------

login_required(login_url='login')
def planning(request):

    planning_vendors = Vendor.objects.filter(services__service_name='Wedding Planning')
    context = {'planning':planning_vendors, }

    return render(request, 'vendor/planning.html', context)

login_required(login_url='login')
def planningView(request, pk):

    vender = get_object_or_404(Vendor, pk=pk)
    service = vender.services.all()

    
    review = ReviewVender.objects.filter(vendor=vender).order_by('-created_at')

    context = {"vender":vender,'service':service,'review':review}

    return render(request, 'vendor/planning_details.html', context)

# PhotosVideosview and their details -----------------------------------------

login_required(login_url='login')
def PhotosVideos(request):

    PhotosVideos_vendors = Vendor.objects.filter(services__service_name='Photography and Videography')
    context = {'PhotosVideos':PhotosVideos_vendors }

    return render(request, 'vendor/PhotosVideos.html', context)

login_required(login_url='login')
def PhotosVideosView(request, pk):

    vender = get_object_or_404(Vendor, pk=pk)
    service = vender.services.all()
    review = ReviewVender.objects.filter(vendor=vender).order_by('-created_at')

    context = {"vender":vender,'service':service,'review':review}
    return render(request, 'vendor/PhotosVideos_details.html', context)

# mehndimakeupview and their details -----------------------------------------

login_required(login_url='login')
def mehndimakeup(request):

    mehndimakeup_vendors = Vendor.objects.filter(services__service_name = 'Makeup and Mehndi')
    context = {'mehndimakeup_vendors':mehndimakeup_vendors}

    return render(request, 'vendor/mehndimakeup.html', context)

login_required(login_url='login')
def mehndimakeupviews(request, pk):

    vender = get_object_or_404(Vendor, pk=pk)
    service = vender.services.all()

    review = ReviewVender.objects.filter(vendor=vender).order_by('-created_at')

    context = {"vender":vender,'service':service,'review':review}

    return render(request, 'vendor/mehndimakeup_details.html', context) 

# artistmanagementview and their details -----------------------------------------

login_required(login_url='login')
def artistmanagement(request):

    artistmanagement_vendors = Vendor.objects.filter(services__service_name = 'Artist Management')
    context = {'artistmanagement_vendors':artistmanagement_vendors}

    return render(request, 'vendor/artistmanagement.html', context)

login_required(login_url='login')
def artistmanagementviews(request, pk):

    vender = get_object_or_404(Vendor, pk=pk)
    service = vender.services.all()

    review = ReviewVender.objects.filter(vendor=vender).order_by('-created_at')

    context = {"vender":vender,'service':service,'review':review}

    return render(request, 'vendor/artistmanagement_details.html', context)


# bandbajaview and their details -----------------------------------------

login_required(login_url='login')
def bandbaja(request):

    bandbaja_vendors = Vendor.objects.filter(services__service_name = 'Band Baja')
    context = {'bandbaja_vendors':bandbaja_vendors}

    return render(request, 'vendor/bandbaja.html', context)

login_required(login_url='login')
def bandbajaviews(request, pk):

    vender = get_object_or_404(Vendor, pk=pk)
    service = vender.services.all()

    review = ReviewVender.objects.filter(vendor=vender).order_by('-created_at')

    context = {"vender":vender,'service':service,'review':review}
    return render(request, 'vendor/bandbajaviews_details.html', context)

# transportlogisticsview and their details -----------------------------------------

login_required(login_url='login')
def transportlogistics(request):

    transportlogistics_vendors = Vendor.objects.filter(services__service_name = 'Transport and Logistics')
    context = {'transportlogistics_vendors':transportlogistics_vendors}

    return render(request, 'vendor/transportlogistics.html', context)

login_required(login_url='login')
def transportlogisticsviews(request, pk):

    vender = get_object_or_404(Vendor, pk=pk)
    service = vender.services.all()

    review = ReviewVender.objects.filter(vendor=vender).order_by('-created_at')

    context = {"vender":vender,'service':service,'review':review}

    return render(request, 'vendor/transportlogisticsviews_details.html', context)

# review -----------------
@login_required(login_url='login')
def reviewVender(request, pk):

    url = request.META.get("HTTP_REFERER")
    if request.method == 'POST':
        try:
            reviews = ReviewVender.objects.get(user__id=request.user.id, vendor__id= pk)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you, Your review has been updated')

            return redirect(url)

        except ReviewVender.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)  
                review.vendor = Vendor.objects.get(id=pk)
                review.user = request.user
                review.save()
                messages.success(request, 'Thank you, your review has been created')
                return redirect(url)
    else:
        form = ReviewForm() 
        context = {'form':form}
    return render(request, 'vendor/decor_details.html', context)    


@login_required(login_url='login')
def venue(request):
    return render(request, 'vendor/venue.html')



