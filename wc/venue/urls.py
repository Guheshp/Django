from django.urls import path
from . import views

urlpatterns = [
    path('',views.venue_list, name='venue_list'),
    path('event_list/',views.event_list, name='event_list'),
    path('addvenue/',views.addvenue, name='addvenue'),

    path('addvenue_info/',views.addvenue_info, name='addvenue_info'),
    path('viewvenue_info/<str:pk>/',views.viewvenue_info, name='viewvenue_info'),
    path('updatevenue_info/<str:pk>/',views.updatevenue_info, name='updatevenue_info'),

    path('add_amenity/<str:pk>/',views.add_amenity, name='add_amenity'),
    path('viewAmenities/<str:pk>/',views.viewAmenities, name='viewAmenities'),
    path('Update_amenities/<int:pk>/',views.Update_amenities, name='Update_amenities'),
    path('Delete_amenities/<str:pk>/',views.Delete_amenities, name='Delete_amenities'),

    path('add_images/<str:pk>/',views.add_images, name='add_images'),
    path('view_image/<str:pk>/',views.view_image, name='view_image'),
    path('Delete_image/<str:pk>/',views.Delete_image, name='Delete_image'),

    path('contact_info/<str:pk>/',views.contact_info, name='contact_info'),
    path('updatecontact_info/<str:pk>/',views.updatecontact_info, name='updatecontact_info'),

    path('category/<str:pk>/',views.category, name='category'),
    path('update_category/<str:pk>/',views.update_category, name='update_category'),

    path('add_restrictions/<str:pk>/',views.add_restrictions, name='add_restrictions'),
    path('viewrestrictions/<str:pk>/',views.viewrestrictions, name='viewrestrictions'),
    path('Update_restrictions/<int:pk>/',views.Update_restrictions, name='Update_restrictions'),
    path('Delete_restrictions/<str:pk>/',views.Delete_restrictions, name='Delete_restrictions'),

    # path('add_amenities_to_venue/<str:pk>',views.add_amenities_to_venue, name='add_amenities_to_venue'),
    # path('addvenue2/',views.addvenue2, name='addvenue2'),
    # path('updateVenue/<str:pk>/',views.updateVenue, name='updateVenue'),
    path('viewallvenue/',views.viewallvenue, name='viewallvenue'),
    path('showvenue/<str:pk>/',views.showvenue, name='showvenue'),
    path('show_user_venue/<str:pk>/',views.show_user_venue, name='show_user_venue'),

    path('user_venues/',views.user_venues, name='user_venues'),
    path('addevent/<str:pk>/',views.addevent, name='addevent'),
    path('update_event/<str:pk>/',views.update_event, name='update_event'),
    path('viewevent/',views.viewevent, name='viewevent'),
    path('booking/<str:pk>',views.booking, name='booking'),
    path('deletebooking/<str:pk>',views.deletebooking, name='deletebooking'),
    path('check_booking/<str:venue_id>',views.check_booking, name='check_booking'),
    path('Info/<str:pk>/',views.Info, name='Info'),
    path('finalbook/<str:pk>/',views.finalbook, name='finalbook'),
    path('payment/',views.payment, name='payment'),
    


]