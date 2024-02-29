from django.shortcuts import render, redirect
from .models import Venue, Event, Booking, VenueImage

from .forms import VenueAddForm

from django.contrib import messages

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


def viewvenue(request):
    venues = Venue.objects.all()
    context = {'venues':venues}
    return render( request, 'venue/viewvenue.html', context)

@login_required(login_url='login')
def showvenue(request,pk):
    venue = Venue.objects.get(id=pk)
    venue_images = VenueImage.objects.filter(venue_id=pk)
    context = {'venue':venue, 'venue_images':venue_images}
    return render(request, 'venue/showvenue.html', context)

def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')

        if query:
            venues = Venue.objects.filter(name__icontains = query)#contains
            return render(request, 'venue/search-bar.html', {'search':venues, 'query': query})
            
        else:  
            print("Receipe not found")
            return render(request, 'venue/search-bar.html',{})
   


