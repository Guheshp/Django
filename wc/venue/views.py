from django.shortcuts import render, redirect
from .models import Venue, Event, Booking, VenueImage, Service, VenueRestrictions, Amenities
from wedding.models import Couples
from django.urls import reverse

from .forms import (VenueInfoForm,
                    UpdateVenueInfoForm,
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

    venueinfo_exists = Venue.objects.filter(user=request.user).exists()
    venue = Venue.objects.filter(user=request.user)

    context = {
            'venueinfo_exists':venueinfo_exists,
            "venue":venue,
        }

    # if request.method == 'POST':
    #     form = VenueInfoForm(request.POST)
    #     if form.is_valid():
    #         venue = form.save(commit=False)
    #         venue.user = request.user 
    #         venue.save() 
    #         venue_name = form.cleaned_data.get('name')
    #         messages.success(request, f"{venue_name} information saved successfully!")

    #         return redirect('add_amenity')
    #     else:
    #         messages.error(request, 'Form submission failed. Please check the data you entered.')
    # else:
    #     form = VenueInfoForm()
    # context = {'form': form}
    return render(request, 'venue/addvenue.html', context)

def VENUE(request):
    venueinfo_exists = Venue.objects.filter(user=request.user).exists()
    venue = Venue.objects.filter(user=request.user)

    context = {'venue':venue,
            'venueinfo_exists':venueinfo_exists, 
            }
    return render(request, 'venue/VENUE.html', context)

def AMENITIES(request):
    venueamenities_exist = Amenities.objects.filter(user = request.user).exists()
    venue = Venue.objects.filter(user=request.user)
    context = {'venueamenities_exist':venueamenities_exist, 'venue':venue}
    return render(request, 'venue/AMENITIES.html', context)

@login_required(login_url='login')
def addvenue_info(request):
    form = VenueInfoForm()
    if request.method == "POST":
        form = VenueInfoForm(request.POST, request.FILES)
        if form.is_valid():
            infoform = form.save(commit=False)
            infoform.user = request.user
            infoform.save()
            venue_name = form.cleaned_data.get('name')
            messages.success(request, f"{venue_name} saved successfully!")
            return redirect('addvenue')
        else:
            messages.error(request, "something went wronge in adding venue information!")
   
        return render(request, 'venue/venueinfo_exists.html', context)

    else:
        form=VenueInfoForm()
    context = {"form":form}
    return render(request, 'venue/addvenue_info.html', context)

@login_required(login_url='login')
def updatevenue_info(request, pk):
    venue = Venue.objects.get(id=pk)
    if request.method == "POST":

        form = UpdateVenueInfoForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            update_venue = form.save(commit=False)
            update_venue.user = request.user
            if 'photo' in request.FILES:
                update_venue.venue_image = request.FILES['photo']
            update_venue.save()
            venue_name = form.cleaned_data.get('name')
            messages.success(request, f"{venue_name} updated successfully!")
            venueinfoview_url = reverse('viewvenue_info', args=[venue.pk])
            return redirect(venueinfoview_url)
        else:
            messages.error(request, "something went wronge in updateing venue!")
    else:
        form = UpdateVenueInfoForm(instance=venue)
    
    context = {'form':form,
               'venue':venue}
    return render(request, 'venue/updatevenue_info.html', context)

@login_required(login_url='login')
def viewvenue_info(request,pk):
    venue_info = Venue.objects.get(id=pk)
    context = {'venue_info':venue_info}
    return render(request, 'venue/viewvenue_info.html', context)



# @login_required(login_url='login')
# def addvenue2(request):
#     if request.method == 'POST':
#         form = VenueInfoForm2(request.POST, request.FILES)
#         if form.is_valid():
#             venue = form.save(commit=False)
#             venue.user = request.user 
#             venue.save() 
#             images = request.FILES.getlist('image')
#             for image in images:
#                 VenueImage.objects.create(venue=venue, image=image)
#             messages.success(request, f"information saved successfully!")

#             return redirect('home')
#         else:
#             messages.error(request, 'Form submission failed. Please check the data you entered.')
#     else:
#         form = VenueInfoForm2()
#     context = {'form': form}
#     return render(request, 'venue/addvenue2.html', context)
@login_required(login_url='login')
def Amenity(request):
    venue = Venue.objects.filter(user=request.user)
    context = {'venue':venue}
    return render(request, 'venue/Amenity.html', context)

@login_required(login_url='login')
def add_amenity(request, pk):
    venue = Venue.objects.get(user=request.user, id=pk) 
    if request.method == 'POST':
        amenity_names = request.POST.getlist('amenity_name')  # Get list of amenity names from form
        
        user = request.user  # Get the current logged-in user
        for name in amenity_names:
            if name.strip():  # Ensure amenity name is not empty
                Amenities.objects.create(user=user,venue=venue, amenity_name=name.strip())  # Create amenity object
        messages.success(request, "Amenities added")        
        return redirect('addvenue')
    
    return render(request, 'venue/add_amenity.html', {'venue':[venue]})

@login_required(login_url='login')
def viewAmenities(request,pk):
    venue = get_object_or_404(Venue, id=pk)
    Amenitie = get_object_or_404(Amenities, id=pk)
    ameneties = Amenities.objects.filter(venue=venue)
    context = {'ameneties':ameneties, 'Amenitie':Amenitie}
    return render(request, 'venue/viewAmenities.html', context)

def Update_amenities(request,pk):
    Amenitie = get_object_or_404(Amenities, id=pk)
    venueamenities_exist = Amenities.objects.filter(id=pk, user = request.user).exists()
    venue = Venue.objects.filter(user=request.user)
    context = {'venueamenities_exist':venueamenities_exist, 'venue':venue}
    return render(request, 'venue/Update_amenities.html', context)

# def add_amenities_to_venue(request, pk):
#     venue = get_object_or_404(Venue, id=pk, user=request.user)
#     amenities = Amenities.objects.filter(user=request.user)
    
#     if request.method == "POST":
#         form = VenueAmenitiesForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             selected_amenities = form.cleaned_data.get('amenitie')
#             if selected_amenities:
#                 for amenity in selected_amenities:
#                     venue_amenity = form.save(commit=False)
#                     venue_amenity.venue = venue
#                     venue_amenity.amenitie = amenity
#                     venue_amenity.save()

#                 messages.success(request, "Amenities added to venue successfully.")
#                 return redirect('addvenue')
#             else:
#                 messages.error(request, "Please select at least one amenity.")
#     else:
#         form = VenueAmenitiesForm(user=request.user)


#     context = {
#         'form': form,
#         'amenities': amenities,
#     }
#     return render(request, 'venue/add_amenities_to_venue.html', context)










    # def add_amenity(request):
    # if request.method == 'POST':
    #     form = AmenityForm(request.POST)
    #      amenity_names = request.POST.getlist('amenity_name')
    #         for amenity_name in amenity_names:
    #             # Create a new form instance for each amenity name
    #             form_instance = AmenityForm({'amenity_name': amenity_name})
    #             if form_instance.is_valid():
    #                 amenity_instance = form_instance.save(commit=False)
    #                 amenity_instance.user = request.user
    #                 amenity_instance.save()
    #             # else:

    #         return redirect('addvenue2')
    #    form = AmenityForm()
    # context = {'form':form}
    # return render(request, 'venue/add_amenity.html',context)

# @login_required(login_url='login')
# def updateVenue(request,pk):
#     venue = get_object_or_404(Venue, id=pk)
#     venue_images = venue.image.all()  # Retrieve all images associated with the venue

#     if request.method == "POST":
#         form = UpdateVenueForm(request.POST, request.FILES, instance=venue)
#         if form.is_valid():
#             update_venue = form.save(commit=False)
#             update_venue.user = request.user
#             if 'venue_image' in request.FILES:
#                 update_venue.venue_image = request.FILES['venue_image']
#             if 'image' in request.FILES:
#                 # Update existing images or add new ones if necessary
#                 for image in request.FILES.getlist('image'):
#                     venue.image.create(image=image)
#             update_venue.save()
#             messages.success(request, 'updated successfully!')
#             venueview_url = reverse('user_venues')
#             return redirect(venueview_url)
#         else:
#             messages.error(request, 'something went wronge')

#     else:
#         form = UpdateVenueForm(instance=venue)
#     context = {'form':form, 'venue':venue, 'venue_images':venue_images}
#     return render(request, 'venue/updatevenue.html', context)


def viewallvenue(request):
    venues = Venue.objects.all().order_by('name')
    # amenitie = amenities.objects.all().order_by('amenity_name')
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
        # 'amenitie': amenitie,
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
    service = Service.objects.filter(venue=venue)
    venue_images = VenueImage.objects.filter(venue_id=pk)
    venueAmenities = Amenities.objects.filter(venue=venue)
    # venueAmenities = VenueAmenities.objects.filter(venue=venue)
    venueRestrictions = VenueRestrictions.objects.filter(venue=venue)

    context = {'venue':venue,
            'venue_images':venue_images,
            'service':service,
            'venueAmenities':venueAmenities, 
            'venueRestrictions':venueRestrictions}
    return render(request, 'venue/show_user_venue.html', context)
   

@login_required(login_url='login')
def addevent(request, pk):
    venue = Venue.objects.get(id=pk)
    amenitie = amenities.objects.all().order_by('amenity_name')

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
    context = {'form':form, 'amenitie':amenitie}
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
        booking_type = request.POST.get('booking_type')



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
                booking_type=booking_type
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
    
    context = {"booking":booking, "form": form, "event":event}
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
 
@login_required(login_url='login')
def Info(request, pk):
    # couples = Couples.objects.filter(user=request.user)
    # events = Event.objects.filter(user=request.user)
    events = get_object_or_404(Event, id=pk)
    bookings = Booking.objects.filter(event=events, user=request.user)
    context = {'events':events, 'bookings':bookings}
    return render (request, 'venue/information.html', context)


@login_required(login_url='login')
def finalbook(request, pk):
    events = get_object_or_404(Event, id=pk)
    context = {'events':events}
    return render (request, 'venue/finalbook.html', context)


@login_required(login_url='login')
def payment(request):
    return render(request, 'venue/payment.html')