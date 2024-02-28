from django.urls import path
from . import views

urlpatterns = [
    path('',views.venue_list, name='venue_list'),

]