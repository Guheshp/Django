from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Vendor, Image, Service
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import VenderRegistrationForm, VenderUpdateForm, ImageForm

# Create your views here.

login_required(login_url='login')
def venderRegistration(request,):

    form = VenderRegistrationForm()

    if request.method == "POST":
        form = VenderRegistrationForm(request.POST, request.FILES)

        if form.is_valid():

            vender = form.save(commit=False)
            vender.user = request.user
            vender.save()
            form.save_m2m()
            messages.success(request, "vender registration form created")

            return redirect("home")
        
    vendor_exists = Vendor.objects.filter(user=request.user).exists()
    
    if vendor_exists:

        # Get the name of the registered vendor

        registered_vendor = Vendor.objects.get(user=request.user)

        messages.success(request,'allready registred')

        context = {"registered_vendor": registered_vendor, 
                 }

        return render(request, 'vendor/vender_exists.html', context)

    else:
        context={"form":form}
    return render(request, 'vendor/registration.html', context)


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
        
    return render(request, 'vendor/updatevender.html', context)


login_required(login_url='login')
def venderViewAll(request):

    vender = Vendor.objects.all().order_by('-id')

    context={"venders":vender}

    return render(request, 'vendor/viewvender_registration.html', context)

login_required(login_url='login')
def deleteVender(request, pk):
    vender = Vendor.objects.get(id=pk)

    if request.method == "POST":

        vender.delete()
        messages.success(request, 'vendor deleted successfully!')
        return redirect("venderviewall")
    
    context = {"vender":vender}
    return render(request, 'vendor/delete_vender.html', context)

login_required(login_url='login')
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
    images = Image.objects.filter(vender=vender)

    context = {"vender":vender, 'images':images, 'service':service}

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
    images = Image.objects.filter(vender=vender)

    context = {"vender":vender, 'images':images, 'service':service}

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
    images = Image.objects.filter(vender=vender)

    context = {"vender":vender, 'images':images, 'service':service}

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
    images = Image.objects.filter(vender=vender)

    context = {"vender":vender, 'images':images, 'service':service}

    return render(request, 'vendor/PhotosVideos_details.html', context)


login_required(login_url='login')
def caterView(request, pk):

    vender = get_object_or_404(Vendor, pk=pk)
    service = vender.services.all()
    images = Image.objects.filter(vender=vender)

    context = {"vender":vender, 'images':images, 'service':service}

    return render(request, 'vendor/cater_details.html', context)


login_required(login_url='login')
def venue(request):
    return render(request, 'vendor/venue.html')


login_required(login_url='login')
def UploadImages(request):
   
    if request.method == "POST":

        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            image_instance = form.save(commit=False)
            
            # Get the registered vendor associated with the current user
            vendor = request.user.vender_profile
            
            # Set the vendor field of the image instance to the retrieved vendor
            image_instance.vender = vendor
            image_instance.save()
            messages.success(request, 'Image uploaded successfully.')
            return redirect('vender_register')
    else:

        form = ImageForm()
    
    context = {'form': form}
    return render(request, 'vendor/images.html', context)