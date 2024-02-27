from django.urls import path
from . import views

urlpatterns = [
    #----------------------- couples registration page--------------------------------
    path('CouplesRegistration/', views.CouplesRegistration, name='CouplesRegistration'),
    
    #----------------------- couples update page--------------------------------

    path('coupleupdate/<str:pk>', views.coupleupdate, name='coupleupdate'),

    #----------------------- all couples page--------------------------------
    path('coupleall/', views.coupleall, name='coupleall'),
    
    #-----------------------view couples in detail page--------------------------------

    path('coupleview/<str:pk>', views.coupleview, name='coupleview'),

    #-----------------------Delete couples page--------------------------------

    path('coupledelete/<str:pk>', views.coupledelete, name='coupledelete'),


] 