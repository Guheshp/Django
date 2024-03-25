from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import datetime
from venue.models import Venue
from django.http import HttpResponse
from django.utils import timezone

from django.db.models import Q

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import uuid

from .utils import generate_invoice_number

from datetime import date


from .models import Enquiry, Date, CopulesDetails, Invoice, InvoiceHistory
from .forms import CouplesdetailsForm, UpdateCouplesdetailsForm, VenuePatmentForm, UpdatePaymentForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def Enquery(request):
    venue = Venue.objects.filter(user=request.user)

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
    context= {'venue':venue}
    return render(request, 'invoice/Eenquery.html', context)


@login_required(login_url='login')
def Enquerylist(request):
    enquiries = Enquiry.objects.all().order_by('-id')
    booked = []
    for enquiry in enquiries:
        couples_details = enquiry.copulesdetails_set.all()
        is_booked = couples_details.exists()
        booked.extend(couples_details)
        enquiry.is_booked = is_booked

    search = request.GET.get('search')
    if search:
        enquiries = enquiries.filter(
            Q(name__icontains=search) |
            Q(phone_number__icontains=search)

            # Q(copulesdetails__name__icontains=search) |  # Example of searching related field
            # Q(copulesdetails__phone_number__icontains=search) |  # Another related field example
            # Q(copulesdetails__dates__icontains=search)  # Another related field example
        )

    context = {'enquiries':enquiries, 'booked':booked, 'search':search}
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

    search = request.GET.get('search')
    if search:
        # Filter CouplesDetails based on bride name or groom name
        couplesdetails = couplesdetails.filter(
            Q(bridename__icontains=search) |
            Q(groomname__icontains=search)|
            Q(enquiry__name__icontains=search)
        )
       

    context = {'couplesdetails': couplesdetails, 'enquiries': enquiries, 'venue': venue, 'search':search}
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

            advance_amt = form.cleaned_data['advance_amt']

            tax_rate = 0.10  # 10%
            tax_amount = advance_amt * tax_rate
            total_amount_with_tax = advance_amt + tax_amount

            new_amt = total_amount_with_tax

            paymentdetails = form.save(commit=False)
            paymentdetails.venue = venue
            paymentdetails.user = request.user
            paymentdetails.enquiry = enquiries
            paymentdetails.new_amt = new_amt
            paymentdetails.invoice_number = invoice_number
            status = request.POST.get('status')

           
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

    venue = get_object_or_404(Venue, pk=venue_id)
    enquiry = get_object_or_404(Enquiry, pk=enquiry_id)

    # Retrieve the corresponding invoice for the venue and enquiry
    invoice = get_object_or_404(Invoice, venue_id=venue_id, enquiry_id=enquiry_id)
    
    # Generate a new invoice number
    new_invoice_number = generate_invoice_number()

    if request.method == 'POST':
        # Process the form submission
        form = UpdatePaymentForm(request.POST, instance=invoice)
        if form.is_valid():
            # Save the updated invoice
            updated_invoice = form.save(commit=False)

            paying_amount = form.cleaned_data['paying_amount']

            tax_rate = 0.10  # 10%
            tax_amount = paying_amount * tax_rate
            total_amount_with_tax = paying_amount + tax_amount

            new_amount = total_amount_with_tax

            # Create an InvoiceHistory instance to record the change
            InvoiceHistory.objects.create(
                invoice=updated_invoice,
                user=request.user,
                new_amount=new_amount,
                paying_amount=paying_amount,
                invoice_number=new_invoice_number,
                date_updated=timezone.now()
            )
            print(new_amount)
            
            invoice.total_amount = invoice.venue.price
            invoice.save()

            messages.success(request, 'Payment updated successfully.')
            return redirect('details', venue_id=venue.id, enquiry_id=enquiry.id)
    else:
        # Render the form with initial data
        form = UpdatePaymentForm(instance=invoice)

    context = {'form': form, 'enquiry':enquiry, 'venue':venue, 'invoice':invoice}

    return render(request, 'invoice/update_payment.html', context)


@login_required(login_url='login')
def payment_list(request):
    invoices = Invoice.objects.all().order_by('-id')
    search = request.GET.get('search')
    if search:
        invoices = invoices.filter(
             Q(enquiry__name__icontains=search)|
             Q(invoice_number__icontains=search)

        )
       

    context = {'invoices':invoices, 'search':search}
    return render(request, 'invoice/payment_list.html', context)


# @login_required(login_url='login')
# def details(request, venue_id, enquiry_id):
#     venue = get_object_or_404(Venue, pk=venue_id)
#     enquiry = Enquiry.objects.get(pk=enquiry_id)
#     invoice = Invoice.objects.filter(venue=venue, enquiry=enquiry).first()
#     invoice_history = InvoiceHistory.objects.filter(invoice=invoice).order_by('-id')
#     coupledetails = enquiry.copulesdetails_set.all()
#     context = {'invoice_history':invoice_history, 'coupledetails':coupledetails,'venue':venue,'enquiry':enquiry, 'invoice':invoice}
#     return render(request, 'invoice/all_details.html', context)


@login_required(login_url='login')
def details(request, venue_id, enquiry_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    enquiry = Enquiry.objects.get(pk=enquiry_id)
    invoice = Invoice.objects.filter(venue=venue, enquiry=enquiry).first()
    invoice_history = InvoiceHistory.objects.filter(invoice=invoice).order_by('-id')

    total_tax_paid = sum(history.tax_payed() for history in invoice_history)

    x = invoice.tax_payed()
    resultx  = x + total_tax_paid

    y = invoice.total_paid_amount()
    resulty  = y+resultx


    search = request.GET.get('search')
    if search:
        invoice_history = invoice_history.filter(
             Q(invoice_number__icontains=search)

        )

    coupledetails = enquiry.copulesdetails_set.all()
    context = {'invoice_history':invoice_history,
            'coupledetails':coupledetails,
            'venue':venue,
            'enquiry':enquiry,
            'invoice':invoice,
            'total_tax_paid':total_tax_paid,
            'resultx':resultx, 
            'resulty':resulty,
            'search':search}
    
    return render(request, 'invoice/details.html', context)



@login_required(login_url='login')
def pdf_report_create(request, venue_id, enquiry_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    enquiry = Enquiry.objects.get(pk=enquiry_id)
    invoice = Invoice.objects.filter(venue=venue, enquiry=enquiry).first()
    invoice_history = InvoiceHistory.objects.filter(invoice=invoice).order_by('-id')
    coupledetails = enquiry.copulesdetails_set.all()

    total_tax_paid = sum(history.tax_payed() for history in invoice_history)

    x = invoice.tax_payed()
    resultx  = x + total_tax_paid

    y = invoice.total_paid_amount()
    resulty  = y + resultx

    template_path = 'invoice/pdfreport.html'
    context = {'invoice_history':invoice_history,
            'coupledetails':coupledetails,
            'venue':venue,
            'enquiry':enquiry,
            'invoice':invoice,
            'resultx':resultx,
            'resulty':resulty}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice-report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required(login_url='login')
def single_pdf_report(request, venue_id, enquiry_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    enquiry = Enquiry.objects.get(pk=enquiry_id)
    invoice = Invoice.objects.filter(venue=venue, enquiry=enquiry).first()
    invoice_history = InvoiceHistory.objects.filter(invoice=invoice).order_by('-id')
    coupledetails = enquiry.copulesdetails_set.all()

    total_tax_paid = sum(history.tax_payed() for history in invoice_history)

    x = invoice.tax_payed()
    resultx  = x + total_tax_paid

    y = invoice.total_paid_amount()
    resulty  = y + resultx

    template_path = 'invoice/single_pdf_report.html'
    context = {'invoice_history':invoice_history,
            'coupledetails':coupledetails,
            'venue':venue,
            'enquiry':enquiry,
            'invoice':invoice,
            'resultx':resultx,
            'resulty':resulty}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="single_invoice-report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
