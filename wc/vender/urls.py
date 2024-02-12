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

    # MehndiandMakeupview and their details -----------------------------------------
    
    path('mehndimakeup/',views.mehndimakeup, name='mehndimakeup'),

    path('mehndimakeupviews/<str:pk>',views.mehndimakeupviews, name='mehndimakeupviews'),

    # artistmanagementviews and their details -----------------------------------------
    
    path('artistmanagement/',views.artistmanagement, name='artistmanagement'),

    path('artistmanagementviews/<str:pk>',views.artistmanagementviews, name='artistmanagementviews'),

    # bandbajaviews and their details -----------------------------------------
    
    path('bandbaja/',views.bandbaja, name='bandbaja'),

    path('bandbajaviews/<str:pk>',views.bandbajaviews, name='bandbajaviews'),

    # transportlogisticsviews and their details -----------------------------------------
    
    path('transportlogistics/',views.transportlogistics, name='transportlogistics'),

    path('transportlogisticsviews/<str:pk>',views.transportlogisticsviews, name='transportlogisticsviews'),



    
    path('uploadimages/',views.UploadImages, name='uploadimages'),



]
