from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import datetime
from venue.models import Venue
from django.http import HttpResponse
from django.utils import timezone

from .utils import generate_invoice_number

from datetime import date


from .models import Enquiry, Date, CopulesDetails, Invoice, InvoiceHistory
from .forms import CouplesdetailsForm, UpdateCouplesdetailsForm, VenuePatmentForm, UpdatePaymentForm
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

    context = {'couplesdetails': couplesdetails, 'enquiries': enquiries, 'venue': venue}
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
                # return redirect('venue_payment',venue.first().id)
                return redirect('home')
    else:
        form = CouplesdetailsForm()
    context = {'form':form, 'enquiry':enquiry, 'venue':venue}
    return render(request, 'invoice/Booking_venue.html', context)

@login_required(login_url='login')
def updateBooking_details(request, pk):
    venue = Venue.objects.filter(user=request.user)
    couplesdetails = get_object_or_404(CopulesDetails, id=pk)

    if couplesdetails.enquiry:
        enquiry = couplesdetails.enquiry
    else:
        return HttpResponse("Enquiry does not exist")
    
    if request.method == 'POST':
        form = UpdateCouplesdetailsForm(request.POST, request.FILES, instance=couplesdetails)
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

                updatedetails = form.save(commit=False)
                updatedetails.enquiry = enquiry
                updatedetails.is_booked = True
                if venue.exists():
                    updatedetails.venue = venue.first()
                updatedetails.save()
                groomname = form.cleaned_data.get('groomname')
                bridename = form.cleaned_data.get('bridename')

                messages.success(request,f"{groomname}'s and {bridename} data saved Successfully.")
                booking_url = reverse('Booking_details', args=[couplesdetails.pk])
                return redirect(booking_url)
                # return redirect('home')
    else:
        form = UpdateCouplesdetailsForm(instance=couplesdetails)
    context = {'form':form, 'couplesdetails':couplesdetails, 'enquiry':enquiry, 'venue':venue}
    return render(request, 'invoice/updateBooking_details.html', context)


@login_required(login_url='login')
def venue_payment(request, pk, name):
    venue = get_object_or_404(Venue, pk=pk)
    enquiries = Enquiry.objects.get(name=name)
    coupledetails = enquiries.copulesdetails_set.all()

    invoice_number = generate_invoice_number()

    if request.method == 'POST':
        form = VenuePatmentForm(request.POST)
        if form.is_valid():
            paymentdetails = form.save(commit=False)
            paymentdetails.venue = venue
            paymentdetails.user = request.user
            paymentdetails.enquiry = enquiries
            paymentdetails.invoice_number = invoice_number
            status = request.POST.get('status')

            advance_amt = form.cleaned_data['advance_amt']

            if advance_amt > venue.price:
                # Add field-level error to the form
                form.add_error('advance_amt', "Advance payment cannot exceed venue price.")

            paymentdetails.status = True if status == 'on' else False 
            paymentdetails.save()

            messages.success(request, f"{paymentdetails.advance_amt} Payment done successfully!")
            return redirect('payment_list')

    else:
        form = VenuePatmentForm(initial={'invoice_number': invoice_number})

    context = {'venue': venue, 'enquiries': enquiries, 'form': form, 'coupledetails':coupledetails}

    return render(request, 'invoice/venue_payment.html', context)


@login_required(login_url='login')
def update_payment(request, venue_id, enquiry_id):
    # Retrieve the corresponding venue and enquiry
    venue = get_object_or_404(Venue, pk=venue_id)
    enquiry = get_object_or_404(Enquiry, pk=enquiry_id)

    # Retrieve the corresponding invoice for the venue and enquiry
    invoice = get_object_or_404(Invoice, venue_id=venue_id, enquiry_id=enquiry_id)
    
    # Generate a new invoice number
    new_invoice_number = generate_invoice_number()

    # old_amount = None
    # if invoice.advance_amt is not None:
    #     old_amount = invoice.advance_amt


    if request.method == 'POST':
        # Process the form submission
        form = UpdatePaymentForm(request.POST, instance=invoice)
        if form.is_valid():
            # Save the updated invoice
            updated_invoice = form.save(commit=False)

            # Calculate the difference between old and new advance_amt values
            paying_amount = form.cleaned_data['paying_amount']
            print("Invoice Advance Amount:", invoice.advance_amt)
            print("Paying Amount:", paying_amount)
            # if paying_amount:
            #     old_amount = invoice.advance_amt + paying_amount
            #     print("Updated Old Amount:", old_amount)
            # else:
            #     old_amount = invoice.advance_amt
            new_amount = paying_amount

            # Create an InvoiceHistory instance to record the change
            InvoiceHistory.objects.create(
                invoice=updated_invoice,
                user=request.user,
                # old_amount=old_amount,
                new_amount=new_amount,
                paying_amount=paying_amount,
                invoice_number=new_invoice_number,
                date_updated=timezone.now()
            )

            
            invoice.total_amount = invoice.venue.price
            invoice.save()

            messages.success(request, 'Payment updated successfully.')
            return redirect('payment_list')
    else:
        # Render the form with initial data
        form = UpdatePaymentForm(instance=invoice)

    context = {'form': form, 'enquiry':enquiry, 'venue':venue, 'invoice':invoice}

    return render(request, 'invoice/update_payment.html', context)
@login_required(login_url='login')
def payment_list(request):
    invoices = Invoice.objects.all().order_by('-id')

    context = {'invoices':invoices}
    return render(request, 'invoice/payment_list.html', context)
