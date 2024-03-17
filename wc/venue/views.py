from django.shortcuts import render, redirect
from .models import Venue, Event, Booking, VenueImage, Service,Restrictions, Amenities, ContactInformation, ServiceCategory
from wedding.models import Couples
from django.urls import reverse

from Invoice.models import Enquiry

from .forms import (VenueInfoForm,
                    UpdateVenueInfoForm,
                    UpdateAmenitiesForm,
                    UpdateRestrictionsForm,
                    UploadImageForm,
                    UpdateImageForm,
                    ContactInformationForm,
                    UpdateContactInformationForm,
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
def addvenue(request, venue_name):
    venueinfo_exists = Venue.objects.filter(user=request.user).exists()
    venue_info = get_object_or_404(Venue, name=venue_name)


    venue = Venue.objects.filter(user=request.user)
    # venueamenities_exist = Amenities.objects.filter(venue__in=venue).exists()
    # venuerestrictions_exist= Restrictions.objects.filter(venue__in=venue)
    contact_exist= ContactInformation.objects.filter(venue__in=venue)
    context = {
            'venueinfo_exists':venueinfo_exists,
            "venue":venue,
            'venue_info':venue_info,
            # 'venueamenities_exist':venueamenities_exist,
            # 'venuerestrictions_exist':venuerestrictions_exist,
            'contact_exist':contact_exist,
        }
    return render(request, 'venue/addvenue.html', context)


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
            return redirect('home')
    
        else:
            messages.error(request, "something went wronge in adding venue information!")
   
    venueinfo_exists = Venue.objects.filter(user=request.user).exists()
    if venueinfo_exists:

        venueinfo_venue= Venue.objects.get(user=request.user)

        context={'venueinfo_venue':venueinfo_venue}

        return render(request, 'venue/venueinfo_exists.html', context)

    else:
        form=VenueInfoForm()
    context = {"form":form, 'venueinfo_exists':venueinfo_exists}
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

@login_required(login_url='login')
def viewvenue_nav(request, venue_name):
    venue_info = get_object_or_404(Venue, name=venue_name)
    context = {'venue_info': venue_info}
    return render(request, 'venue/viewvenue_nav.html', context)


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
def add_amenity(request, pk):
    # amenities_exists = Amenities.objects.filter(user=request.user).exists()
    venue = Venue.objects.get(user=request.user, id=pk) 
    if request.method == 'POST':
        amenity_names = request.POST.getlist('amenity_name')  # Get list of amenity names from form
        user = request.user  
        for name in amenity_names:
            if name.strip():  # Ensure amenity name is not empty
                Amenities.objects.create(user=user,venue=venue, amenity_name=name.strip())  # Create amenity object
        messages.success(request, "Amenities added")   

        return redirect('home')
    return render(request, 'venue/add_amenity.html', {'venue':[venue]})

@login_required(login_url='login')
def viewAmenities(request,pk):
    venue = Venue.objects.filter(user=request.user)
    amenities = Amenities.objects.filter(user=request.user, venue_id=pk)
    context = {'amenities':amenities, 'venue':venue}
    return render(request, 'venue/viewAmenities.html', context)

@login_required(login_url='login')
def Delete_amenities(request, pk):
    amenity = get_object_or_404(Amenities, id=pk)
    if request.method == 'POST':
        amenity.delete()
        messages.success(request, 'amenity deleted successfully!')
        # return redirect("viewAmenities")
        venue_pk = amenity.venue.pk
        return redirect('viewAmenities', pk=venue_pk)
    context = {'amenity':amenity}
    return render(request, 'venue/Delete_amenities.html', context)


@login_required(login_url='login')
def Update_amenities(request,pk):
    amenity = get_object_or_404(Amenities, id=pk)

    if request.method == "POST":
        form = UpdateAmenitiesForm(request.POST, instance=amenity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Amenity updated successfully!')
            return redirect('home')  
        else:
            messages.error(request, 'Something went wrong while updating the amenity.')
    else:
        form = UpdateAmenitiesForm(instance=amenity)

    context = {'form': form, 'amenity':amenity}
    return render(request, 'venue/Update_amenities.html', context)


@login_required(login_url='login')
def add_restrictions(request, pk):
    venue = Venue.objects.get(user=request.user, id=pk) 
    if request.method == 'POST':
        restriction_names = request.POST.getlist('restriction_name')  # Get list of amenity names from form
        user = request.user  
        for name in restriction_names:
            if name.strip():  # Ensure amenity name is not empty
                Restrictions.objects.create(user=user,venue=venue, restriction_name=name.strip())  # Create amenity object
        messages.success(request, "Restrictions added")        
        return redirect('home')
    return render(request, 'venue/add_restrictions.html', {'venue':[venue]})

@login_required(login_url='login')
def viewrestrictions(request,pk):
    venue = Venue.objects.filter(user=request.user)

    restrictions = Restrictions.objects.filter(user=request.user, venue_id=pk)
    context = {'restrictions':restrictions, 'venue':venue}
    return render(request, 'venue/viewrestrictions.html', context)


@login_required(login_url='login')
def Update_restrictions(request,pk):
    restrictions = get_object_or_404(Restrictions, id=pk)
    if request.method == "POST":
        form = UpdateRestrictionsForm(request.POST, instance=restrictions)
        if form.is_valid():
            form.save()
            messages.success(request, 'restrictions updated successfully!')
            return redirect('home')  
        else:
            messages.error(request, 'Something went wrong while updating the amenity.')
    else:
        form = UpdateRestrictionsForm(instance=restrictions)

    context = {'form': form, 'restrictions':restrictions}
    return render(request, 'venue/Update_restrictions.html', context)


@login_required(login_url='login')
def Delete_restrictions(request, pk):
    restrictions = get_object_or_404(Restrictions, id=pk)
    if request.method == 'POST':
        restrictions.delete()
        messages.success(request, 'restrictions deleted successfully!')
        return redirect("home")
    context = {'restrictions':restrictions}
    return render(request, 'venue/Delete_restrictions.html', context)


@login_required(login_url='login')
def add_images(request, pk):
    venue = Venue.objects.get(user=request.user, id=pk) 
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('image')
            for image in images:
                VenueImage.objects.create(venue=venue, image=image)
            messages.success(request, f"information saved successfully!")
            return redirect('home')
    else:
        form =   UploadImageForm()    
    context = {'form':form}  
    return render (request, 'venue/add_images.html', context)


@login_required(login_url='login')
def view_image(request, pk):
    venue = Venue.objects.get(user=request.user, id=pk) 

    venue_images = venue.image.all()  # Retrieve all images associated with the venue

    if request.method == "POST":
        form = UpdateImageForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            update_venue = form.save(commit=False)
            update_venue.user = request.user
            if 'image' in request.FILES:
                # Update existing images or add new ones if necessary
                for image in request.FILES.getlist('image'):
                    venue.image.create(image=image)
            update_venue.save()
            messages.success(request, 'updated images successfully!')
            return redirect('home')
        else:
            messages.error(request, 'something went wronge')
    else:
        form = UpdateImageForm(instance=venue)

    context = {'form':form,'venue':venue, 'venue_images':venue_images}
    return render(request, 'venue/view_image.html', context)


@login_required(login_url='login')
def Delete_image(request, pk):
    image = get_object_or_404(VenueImage, id=pk)
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'image deleted successfully!')
        return redirect("home")
    context = {'image':image}
    return render(request, 'venue/Delete_image.html', context)


@login_required(login_url='login')
def contact_info(request, pk):

    venue = get_object_or_404(Venue, id=pk)
    if request.method == 'POST':
        form = ContactInformationForm(request.POST)
        if form.is_valid():
            contact=form.save(commit=False)
            contact.user = request.user
            contact.venue = venue
            contact.save()
            contact_email = form.cleaned_data.get('email')
            messages.success(request, f"{contact_email} information saved successfully!")
            return redirect('home')
        
    contactinfo_exists = ContactInformation.objects.filter(user=request.user).exists()

    if contactinfo_exists:

        contactinfo= ContactInformation.objects.get(user=request.user, venue=venue)

        context={'contactinfo':contactinfo}

        return render(request, 'venue/contactinfo_exists.html', context)
    else:

        form=ContactInformationForm()
    context= {'form':form, 'contactinfo_exists':contactinfo_exists}
    return render(request, 'venue/contact_info.html', context)


@login_required(login_url='login')
def updatecontact_info(request, pk):
    venue = get_object_or_404(Venue, id=pk)
    contact = get_object_or_404(ContactInformation, venue=venue)
    if request.method == "POST":
        form = UpdateContactInformationForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'updated successfully!')
            return redirect("home")
    else:
        form = UpdateContactInformationForm(instance=contact)
    context = {'form':form, 'contact':contact}
    return render(request, 'venue/updatecontact_info.html', context)


@login_required(login_url='login')
def category(request, pk):
    venue = get_object_or_404(Venue, id=pk)

    categoryservice = ServiceCategory.objects.all()
    if request.method == "POST":
        max_capacity = request.POST.get('max_capacity')
        max_capacity_outdoor = request.POST.get('max_capacity_outdoor')
        max_capacity_indoor = request.POST.get('max_capacity_indoor')
        outdoor = request.POST.get('outdoor') == 'true'
        indoor = request.POST.get('indoor') == 'true'

        category_names = [x.name for x in  ServiceCategory.objects.all()]

        category_ids= []

        for x in category_names:
            category_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print('error')
        
        categorys = Service.objects.create(
            venue = venue,
            max_capacity=max_capacity,
            max_capacity_outdoor=max_capacity_outdoor,
            max_capacity_indoor=max_capacity_indoor,
            outdoor=outdoor,
            indoor=indoor,
        )

        categorys.save()

        for x in category_ids:
            categorys.category.add(ServiceCategory.objects.get(id=x))
        messages.success(request, 'done')
        return redirect('home')
            
    category_exists = Service.objects.filter(venue=venue).exists()
    if category_exists:

        category_exists= Service.objects.get(venue=venue)

        context={'category_exists':category_exists}

        return render(request, 'venue/category_exists.html', context)

    else:

        context = {'categoryservice':categoryservice, 'category_exists':category_exists}
        return render (request, 'venue/category.html', context)

@login_required(login_url='login')
def update_category(request, pk):
    # Retrieve the service object based on the provided primary key
    venue = get_object_or_404(Venue, id=pk)

    service = get_object_or_404(Service, venue=venue)
    
    # Retrieve all service categories from the database
    categoryservice = ServiceCategory.objects.all()
    
    if request.method == "POST":
        # Retrieve form data
        max_capacity = request.POST.get('max_capacity')
        max_capacity_outdoor = request.POST.get('max_capacity_outdoor')
        max_capacity_indoor = request.POST.get('max_capacity_indoor')
        
        # Convert checkbox values to boolean
        outdoor = request.POST.get('outdoor') == 'true'
        indoor = request.POST.get('indoor') == 'true'

        # Retrieve selected category IDs
        category_ids = [int(request.POST.get(category.name)) for category in categoryservice if request.POST.get(category.name)]
        
        # Update service object attributes
        service.max_capacity = max_capacity
        service.max_capacity_outdoor = max_capacity_outdoor
        service.max_capacity_indoor = max_capacity_indoor
        service.outdoor = outdoor
        service.indoor = indoor
        
        # Clear existing categories and add selected categories
        service.category.clear()
        for category_id in category_ids:
            service.category.add(category_id)
        
        # Save the updated service object
        service.save()
        
        # Display success message
        messages.success(request, 'Service category updated successfully!')
        
        # Redirect the user to the 'addvenue' page
        return redirect('home')
    
    # Pass the service object and service categories to the template context
    context = {'service': service, 'categoryservice': categoryservice}
    
    # Render the update_category.html template with the provided context
    return render(request, 'venue/update_category.html', context)


def viewallvenue(request):
    venues = Venue.objects.all().order_by('name')
    # venue_for = Venue.objects.filter(user=request.user)
    # service = Service.objects.filter(venue__in=venue_for)

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
        # 'service':service,
        'form': form,
        'date': date,
        'no_venues_message':no_venues_message,
    }

    return render(request, 'venue/viewallvenue.html', context)

# @login_required(login_url='login')
def showvenue(request,pk):
    venue = Venue.objects.get(id=pk)
    service = Service.objects.filter(venue=venue)
    venue_images = VenueImage.objects.filter(venue_id=pk)
    venueAmenities = Amenities.objects.filter(venue=venue)
    venueAmenities = Amenities.objects.filter(venue=venue)
    venueRestrictions = Restrictions.objects.filter(venue=venue)
    contactinfo = ContactInformation.objects.filter(venue=venue)
    # venueAmenities = VenueAmenities.objects.filter(venue=venue)

    context = {'venue':venue,
            'venue_images':venue_images,
            'service':service,
            'venueAmenities':venueAmenities, 
            'venueRestrictions':venueRestrictions,
            'contactinfo':contactinfo}
    return render(request, 'venue/showvenue.html', context)

@login_required(login_url='login')
def user_venues(request):
    user_name = request.user
    user_venues = Venue.objects.filter(user=request.user).order_by('name')
    enquiry_count = Enquiry.objects.all().count()
    context = {'user_venues': user_venues, 'user_name':user_name, 'enquiry_count':enquiry_count}
    return render(request, 'venue/user_venues.html', context)

@login_required(login_url='login')
def show_user_venue(request,pk):
    venue = Venue.objects.get(id=pk)
    service = Service.objects.filter(venue=venue)
    venue_images = VenueImage.objects.filter(venue_id=pk)
    venueAmenities = Amenities.objects.filter(venue=venue)
    venueAmenities = Amenities.objects.filter(venue=venue)
    venueRestrictions = Restrictions.objects.filter(venue=venue)
    contactinfo = ContactInformation.objects.filter(venue=venue)
    # venueAmenities = VenueAmenities.objects.filter(venue=venue)

    context = {'venue':venue,
            'venue_images':venue_images,
            'service':service,
            'venueAmenities':venueAmenities, 
            'venueRestrictions':venueRestrictions,
            'contactinfo':contactinfo}
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