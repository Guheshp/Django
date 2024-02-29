from django.urls import path
from . import views

urlpatterns = [
    path('',views.venue_list, name='venue_list'),
    path('event_list/',views.event_list, name='event_list'),
    path('addvenue/',views.addvenue, name='addvenue'),
    path('viewvenue/',views.viewvenue, name='viewvenue'),
    path('showvenue/<str:pk>',views.showvenue, name='showvenue'),
    path('search/',views.search, name='search'),

]