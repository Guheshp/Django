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
    
    # caterview and their details -----------------------------------------

    path('catering/',views.catering, name='catering'),

    path('caterView/<str:pk>',views.caterView, name='caterView'),


    # decorview and their details -----------------------------------------

    path('decor/',views.decor, name='decor'),

    path('decorView/<str:pk>',views.decorView, name='decorView'),
    
    # planningview and their details -----------------------------------------

    path('planning/',views.planning, name='planning'),

    path('planningView/<str:pk>',views.planningView, name='planningView'),

 # PhotosVideosview and their details -----------------------------------------

    path('PhotosVideos/',views.PhotosVideos, name='PhotosVideos'),

    path('PhotosVideosView/<str:pk>',views.PhotosVideosView, name='PhotosVideosView'),


    
    path('uploadimages/',views.UploadImages, name='uploadimages'),



]
