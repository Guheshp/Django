from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('',views.Home, name='home'),

    path('register/',views.Register, name='register'),
    
    path('login/',views.Login, name='login'),

    path('logout/',views.Logout, name='logout'),

    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),

    path('acc_active_email_complete',views.acc_active_email_complete, name='acc_active_email_complete'),

    path('acc_active_email_invalid',views.acc_active_email_invalid, name='acc_active_email_invalid'),

#  password reset 

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='acc/reset_password.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='acc/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='acc/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='acc/password_reset_complete.html'),name='password_reset_complete'),
   
]


