from django.urls import path
from . import views

urlpatterns = [
    #----------------------- couples registration page--------------------------------
    path('CouplesRegistration/', views.CouplesRegistration, name='CouplesRegistration'),
    
    #----------------------- couples registration page--------------------------------

    path('coupleupdate/<str:pk>', views.coupleupdate, name='coupleupdate'),

    #----------------------- couples  page--------------------------------

    path('coupleupdate/<str:pk>', views.coupleupdate, name='coupleupdate'),
] 