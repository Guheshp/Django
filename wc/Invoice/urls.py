from django.urls import path
from . import views

urlpatterns = [

    path('',views.Enquery, name='Enquery'),
    path('Enquerylist/',views.Enquerylist, name='Enquerylist'),
    path('enquiryUpdate/<str:enquiry_id>/',views.update_enquiry, name='enquiryUpdate'),
    path('delete_enquiry/<str:pk>/',views.delete_enquiry, name='delete_enquiry'),

    path('Booking/',views.Booking, name='Booking'),
    path('Booking_venue/<str:pk>/',views.Booking_venue, name='Booking_venue'),
    path('Booking_details/<str:pk>/',views.Booking_details, name='Booking_details'),
    path('updateBooking_details/<str:pk>/',views.updateBooking_details, name='updateBooking_details'),

    path('venue_payment/<str:pk>/<str:name>/',views.venue_payment, name='venue_payment'),
    path('update_payment/<str:venue_id>/<str:enquiry_id>/', views.update_payment, name='update_payment'),
    path('update_first_payment/<str:venue_id>/<str:enquiry_id>/', views.update_first_payment, name='update_first_payment'),
    path('payment_list/',views.payment_list, name='payment_list'),

    path('update_invoice_history/<str:venue_id>/<str:enquiry_id>/<str:invoice_history_id>/', views.update_invoice_history, name='update_invoice_history'),
    # path('details/<str:venue_id>/<str:enquiry_id>/',views.details, name='details'),

    path('details/<str:venue_id>/<str:enquiry_id>/',views.details, name='details'),
    path('pdf_report_create/<str:venue_id>/<str:enquiry_id>/',views.pdf_report_create, name='pdf_report_create'),

    path('single_pdf_report/<str:invoice_history_id>/',views.single_pdf_report, name='single_pdf_report'),
    path('single_pdf/<str:invoice_history_id>/',views.single_pdf, name='single_pdf'),

    path('invoive1_pdf/<str:invoice_id>/',views.invoive1_pdf, name='invoive1_pdf'),
    path('invoive1_pdf_report/<str:invoice_id>/',views.invoive1_pdf_report, name='invoive1_pdf_report'),


    path('calender/',views.calender, name='calender'),




]

