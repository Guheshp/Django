from django.shortcuts import render, redirect
from .models import Venue, Event, Booking, VenueImage, amenities
from wedding.models import Couples
from django.urls import reverse

from .forms import (VenueAddForm, 
                    UpdateVenueForm,
                    AddEventForm,
                    UpdateEventForm,
                    CheckAvailabilityForm,
                    CancelVenueForm)
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.db import IntegrityError

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
    amenitie = amenities.objects.all().order_by('amenity_name')
    no_venues_message = None

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    Amenities = request.GET.getlist('amenities')

    if sort_by == "Asc":
        venues = venues.order_by('booking_cost')
    elif sort_by == "Dsc":
        venues = venues.order_by('-booking_cost')
    
    if search:
        venues = venues.filter(
            Q(name__icontains=search) |
            Q(city__icontains=search) |
            Q(hall_counts__icontains=search)
        )
    
    if len(Amenities):
        venues = venues.filter(amenities__amenity_name__in=Amenities).distinct()
    
    if not venues:
        no_venues_message = 'No venues found.'

    form = CheckAvailabilityForm()
    date = None

    if request.method == 'POST':
        form = CheckAvailabilityForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            print(date)
            # Query available venues based on the selected date
            available_venues = venues.exclude(
                id__in=Booking.objects.filter(
                    Q(start_date__lte=date, end_date__gte=date) |
                    Q(start_date__gte=date, end_date__lte=date)
                ).values_list('venue_id', flat=True)
            )

            if available_venues:
                messages.success(request, f"Venues are available on {date} selected date.")
            else:
                messages.warning(request, 'No venues are available on selected date.')
        else:
            messages.error(request, 'Please enter a valid date.')

    else:
        available_venues = venues  # Show all venues if no date selected

    context = {
        'venues': available_venues,
        'amenitie': amenitie,
        'sort_by': sort_by,
        'search': search,
        'Amenities': Amenities,
        'form': form,
        'date': date,
        'no_venues_message':no_venues_message,
    }

    return render(request, 'venue/viewallvenue.html', context)

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
            return redirect("viewevent")
        else:
            messages.error(request, 'somwthing went wronge while adding event!')
    else:
        form = AddEventForm()
    context = {'form':form}
    return render(request, 'venue/addevent.html', context)


@login_required(login_url='login')
def update_event(request, pk):
    event = get_object_or_404(Event, id=pk)

    form = UpdateEventForm(instance=event)
    if request.method == "POST":
        form = UpdateEventForm( request.POST, instance=event)
        if form.is_valid():
            form.save()
            event_name = form.cleaned_data.get('name')

            messages.success(request, f"{event_name} is updated successfully!")
            return redirect("viewevent")
    else:
        form = UpdateEventForm(instance=event)

    context = {'event':event, 'form':form}
    return render(request, 'venue/update_event.html', context)

def viewevent(request,):
    couples = Couples.objects.filter(user=request.user)
    events = Event.objects.filter(user=request.user).order_by('-id')
    bookings = Booking.objects.filter(user=request.user)

    context = {'events':events, 'couples':couples, 'bookings':bookings}
    return render(request, 'venue/viewevent.html', context)

@login_required(login_url='login')
def booking(request, pk):
    if request.method == "POST":
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        event = get_object_or_404(Event, id=pk)
        venue = event.venue

        if checkout < checkin:
                messages.error(request, 'End date must be after the start date')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # Check if the venue is already booked for the selected dates
        if not check_booking(checkin, checkout, venue.id):
            messages.warning(request, 'Venue is already booked for these dates!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        
        # Create a new booking
        try:
            Booking.objects.create(
                venue=venue,
                event=event,
                user=request.user,
                start_date=checkin,
                end_date=checkout,
                is_booked=True,
                booking_type='pre paid'
            )  
            messages.success(request, 'Your booking has been saved')
            return redirect('viewevent')

        except IntegrityError:
            messages.error(request, 'An error occurred while saving your booking')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return redirect('home') 


@login_required(login_url='login')
def deletebooking(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    event = booking.event
    venue = event.venue

    if request.method == "POST":
        form = CancelVenueForm(request.POST)
        if form.is_valid():
            cancel = form.save(commit=False)
            cancel.user = request.user
            cancel.venue = venue
            cancel.event = event
            cancel.save()
            booking.delete()
        messages.success(request, 'Booking canceled successfully!')
        return redirect("viewevent")
    else:
        form = CancelVenueForm()
    
    context = {"booking":booking, "form": form}
    return render(request, "venue/deletebooking.html", context)


def check_booking(start_date, end_date, venue_id):
    # Filter existing bookings that overlap with the provided dates
    bookings_overlap = Booking.objects.filter(
        venue__id=venue_id,
        start_date__lte=end_date,
        end_date__gte=start_date
    )
    
    # If there are any overlapping bookings, return False
    if bookings_overlap.exists():
        return False
    
    return True
 

def Info(request, pk):
    # couples = Couples.objects.filter(user=request.user)
    # events = Event.objects.filter(user=request.user)
    events = get_object_or_404(Event, id=pk)
    bookings = Booking.objects.filter(event=events, user=request.user)
    context = {'events':events, 'bookings':bookings}
    return render (request, 'venue/information.html', context)

def finalbook(request, pk):
    events = get_object_or_404(Event, id=pk)
    context = {'events':events}
    return render (request, 'venue/finalbook.html', context)