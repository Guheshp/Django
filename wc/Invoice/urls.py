from django.urls import path
from . import views

urlpatterns = [
    path('',views.Enquery, name='Enquery'),
    path('Enquerylist',views.Enquerylist, name='Enquerylist'),
]