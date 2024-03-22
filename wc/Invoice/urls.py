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

    path('venue_payment/<str:pk>/',views.venue_payment, name='venue_payment'),
    path('update_payment/<str:invoice_id>/',views.update_payment, name='update_payment'),
    path('payment_list/',views.payment_list, name='payment_list'),

   path('enquiry_venue_payment_history/<int:enquiry_id>/<int:venue_id>/', views.enquiry_venue_payment_history, name='enquiry_venue_payment_history'),


]

