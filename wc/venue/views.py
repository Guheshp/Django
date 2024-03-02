from django.shortcuts import render, redirect
from .models import Venue, Event, Booking, VenueImage
from django.urls import reverse

from .forms import VenueAddForm, UpdateVenueForm, AddEventForm

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.


def venue_list(request):
    venues = Venue.objects.all()
    context = {
        'venues':venues
    }
    return render(request, 'venue/venue_list.html', context)

def event_list(request):
    events = Event.objects.all()
    context = {'events':events}
    return render(request, 'venue/events_list.html', context)


@login_required(login_url='login')
def addvenue(request):
    if request.method == 'POST':
        
        form = VenueAddForm(request.POST, request.FILES)

        if form.is_valid():
            venue = form.save(commit=False)
            venue.user = request.user 
            venue.save() 
            images = request.FILES.getlist('image')  # Retrieve the list of uploaded images

            for image in images:
                VenueImage.objects.create(venue=venue, image=image)
            messages.success(request, 'Your Venue submitted successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Form submission failed. Please check the data you entered.')
    else:
        form = VenueAddForm()

    context = {'form':form}
    return render(request, 'venue/addvenue.html', context)

@login_required(login_url='login')
def updateVenue(request,pk):
    venue = get_object_or_404(Venue, id=pk)
    venue_images = venue.image.all()  # Retrieve all images associated with the venue

    if request.method == "POST":
        form = UpdateVenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            update_venue = form.save(commit=False)
            update_venue.user = request.user
            if 'venue_image' in request.FILES:
                update_venue.venue_image = request.FILES['venue_image']
            if 'image' in request.FILES:
                # Update existing images or add new ones if necessary
                for image in request.FILES.getlist('image'):
                    venue.image.create(image=image)
            update_venue.save()
            messages.success(request, 'updated successfully!')
            venueview_url = reverse('user_venues')
            return redirect(venueview_url)
        else:
            messages.error(request, 'something went wronge')

    else:
        form = UpdateVenueForm(instance=venue)
    context = {'form':form, 'venue':venue, 'venue_images':venue_images}
    return render(request, 'venue/updatevenue.html', context)

def viewallvenue(request):
    venues = Venue.objects.all().order_by('name')
    context = {'venues':venues}
    return render( request, 'venue/viewallvenue.html', context)

# @login_required(login_url='login')
def showvenue(request,pk):
    venue = Venue.objects.get(id=pk)
    venue_images = VenueImage.objects.filter(venue_id=pk)
    context = {'venue':venue, 'venue_images':venue_images}
    return render(request, 'venue/showvenue.html', context)

@login_required(login_url='login')
def user_venues(request):
    user_name = request.user
    user_venues = Venue.objects.filter(user=request.user).order_by('name')
    context = {'user_venues': user_venues, 'user_name':user_name}
    return render(request, 'venue/user_venues.html', context)

@login_required(login_url='login')
def show_user_venue(request,pk):
    venue = Venue.objects.get(id=pk)
    venue_images = VenueImage.objects.filter(venue_id=pk)
    context = {'venue':venue, 'venue_images':venue_images}
    return render(request, 'venue/show_user_venue.html', context)
   
def search(request):
    # if request.method == 'GET':
        query = request.GET.get('query')

        if query:
            venues = Venue.objects.filter(name__icontains = query)#contains
            return render(request, 'venue/search-bar.html', {'search':venues, 'query': query})
            
        else:  
            print("Receipe not found")
            return render(request, 'venue/search-bar.html',{})


@login_required(login_url='login')
def addevent(request, pk):
    venue = Venue.objects.get(id=pk)
    if request.method == "POST":

        form = AddEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.venue = venue
            event.save()
            messages.success(request, "event added successfully!")
            return redirect("home")
        else:
            messages.error(request, 'somwthing went wronge while adding event!')
    else:
        form = AddEventForm()
    context = {'form':form}
    return render(request, 'venue/addevent.html', context)


@login_required(login_url="login")
def viewevent(request):
    events = Event.objects.filter(user=request.user)
    context = {'events':events}
    return render(request, 'venue/viewevent.html', context)