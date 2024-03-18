from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import datetime
from venue.models import Venue

from datetime import date


from .models import Enquiry, Date, CopulesDetails
from .forms import CouplesdetailsForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def Enquery(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        dates = request.POST.getlist('date')  # Get list of dates

        # Ensure that name and phone number are provided
        if not name or not phone_number:
            messages.error(request, "Name and phone number are required.")
            return redirect('home')  # Replace 'your_form_view_name' with the name of your form view

        # Ensure that at least one date is provided
        if not dates:
            messages.error(request, "Please provide at least one date.")
            return redirect('home')  # Replace 'your_form_view_name' with the name of your form view

        # Create Enquiry object
        enquiry = Enquiry.objects.create(name=name, phone_number=phone_number)

        # Add dates to the Enquiry object
        for date_str in dates:
            date_obj, created = Date.objects.get_or_create(date=date_str)
            enquiry.dates.add(date_obj)

        messages.success(request, "Enquiry information added successfully!")
        return redirect('home')
    return render(request, 'invoice/Eenquery.html')


@login_required(login_url='login')
def Enquerylist(request):
    enquiries = Enquiry.objects.all().order_by('-id')
    booked = []
    for enquiry in enquiries:
        couples_details = enquiry.copulesdetails_set.all()
        is_booked = couples_details.exists()
        booked.extend(couples_details)
        enquiry.is_booked = is_booked


    # for enquiry in enquiries:
    #     print(enquiry.name)
        # for date in enquiry.dates.all():
        #     print(date.date)

    context = {'enquiries':enquiries, 'booked':booked}
    return render(request, 'invoice/Enquerylist.html', context)


@login_required(login_url='login')
def update_enquiry(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, pk=enquiry_id)

    if request.method == "POST":
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
      

        # Update enquiry details
        enquiry.name = name
        enquiry.phone_number = phone_number

        enquiry.save()

        messages.success(request, "Enquiry information updated successfully!")
        return redirect('home')

    return render(request, 'invoice/enquiryUpdate.html', {'enquiry': enquiry})


@login_required(login_url='login')
def delete_enquiry(request, pk):
    enquiry = get_object_or_404(Enquiry, id=pk)
    if request.method == 'POST':
        enquiry.delete()
        messages.success(request, 'enquiry deleted successfully!')
        return redirect('Enquerylist')
    context = {'enquiry':enquiry}

    return render(request, 'invoice/delete_enquiry.html', context)


@login_required(login_url='login')
def Booking(request):
    couplesdetails = CopulesDetails.objects.all().order_by('-id')
    enquiries = Enquiry.objects.all().order_by('-id')
    venue = Venue.objects.filter(user=request.user)
    context = {'couplesdetails':couplesdetails, 'enquiries':enquiries, 'venue':venue}
    return render(request, 'invoice/booking_list.html', context)


@login_required(login_url='login')
def Booking_details(request, pk):
    couplesdetails = CopulesDetails.objects.get(id=pk)
    groomDOB = couplesdetails.groomDOB
    brideDOB = couplesdetails.brideDOB

    groomDOB = (date.today() - groomDOB).days // 365
    brideDOB = (date.today() - brideDOB).days // 365

    context = {'couplesdetails':couplesdetails, 'groomDOB':groomDOB, 'brideDOB':brideDOB}
    return render(request, 'invoice/Booking_details.html', context)

@login_required(login_url='login')
def Booking_venue(request, pk):

    venue = Venue.objects.filter(user=request.user)
    enquiry = get_object_or_404(Enquiry, id=pk)

    if request.method == "POST":
        form = CouplesdetailsForm(request.POST, request.FILES)
        if form.is_valid():

            groomDOB = form.cleaned_data.get('groomDOB')
            brideDOB = form.cleaned_data.get('brideDOB')

            groomDOB = (date.today() - groomDOB).days // 365
            brideDOB = (date.today() - brideDOB).days // 365

            if groomDOB < 21:
                form.add_error('groomDOB', 'Groom must be at least 21 years old.')
            if brideDOB < 18:
                form.add_error('brideDOB', 'Bride must be at least 18 years old.')
            
            if not form.errors:

                details = form.save(commit=False)
                details.enquiry = enquiry
                details.is_booked = True
                if venue.exists():
                    details.venue = venue.first()
                details.save()
                groomname = form.cleaned_data.get('groomname')
                bridename = form.cleaned_data.get('bridename')

                messages.success(request,f"{groomname}'s and {bridename} data saved Successfully.")
                return redirect('home')
    else:
        form = CouplesdetailsForm()
    context = {'form':form, 'enquiry':enquiry, 'venue':venue}
    return render(request, 'invoice/Booking_venue.html', context)