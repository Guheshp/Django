from django.urls import path
from . import views

urlpatterns = [
    path('',views.venue_list, name='venue_list'),
    path('event_list/',views.event_list, name='event_list'),
    path('addvenue/',views.addvenue, name='addvenue'),
    path('updateVenue/<str:pk>/',views.updateVenue, name='updateVenue'),
    path('viewallvenue/',views.viewallvenue, name='viewallvenue'),
    path('showvenue/<str:pk>/',views.showvenue, name='showvenue'),
    path('show_user_venue/<str:pk>/',views.show_user_venue, name='show_user_venue'),
    path('search/',views.search, name='search'),
    path('user_venues/',views.user_venues, name='user_venues'),
    path('addevent/<str:pk>/',views.addevent, name='addevent'),
    path('viewevent/',views.viewevent, name='viewevent'),



]