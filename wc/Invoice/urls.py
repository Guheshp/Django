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
]