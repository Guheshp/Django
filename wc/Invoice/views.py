from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import datetime

from .models import Enquiry, Date
from .forms import UpdateEnquiryForm
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
    for enquiry in enquiries:
        print(enquiry.name)
        for date in enquiry.dates.all():
            print(date.date)

    context = {'enquiries':enquiries}
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
        return redirect('home')
    context = {'enquiry':enquiry}

    return render(request, 'invoice/delete_enquiry.html', context)
