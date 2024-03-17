from django.urls import path
from . import views

urlpatterns = [
    path('',views.Enquery, name='Enquery'),
    path('Enquerylist/',views.Enquerylist, name='Enquerylist'),
    path('enquiryUpdate/<str:enquiry_id>',views.update_enquiry, name='enquiryUpdate'),
    path('delete_enquiry/<str:pk>',views.delete_enquiry, name='delete_enquiry'),
]