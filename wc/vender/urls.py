from django.urls import path
from . import views

urlpatterns = [
    path('vender_register/',views.venderRegistration, name='vender_register'),
    
    path('venderviewall/',views.venderViewAll, name='venderviewall'),

    path('venderview/<str:pk>',views.vebderView, name='venderview'),

    path('updatevender/<str:pk>',views.VenderUpdate, name='updatevender'),

    path('deletevender/<str:pk>',views.deleteVender, name='deletevender'),
    
    path('services/',views.services, name='services'),

    path('venue/',views.venue, name='venue'),
    
    path('catering/',views.catering, name='catering'),

    path('caterView/<str:pk>',views.caterView, name='caterView'),
    
    path('uploadimages/',views.UploadImages, name='uploadimages'),



]
