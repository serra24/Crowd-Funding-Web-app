from django.urls import path, include  # Import include function
from . import views
from django.contrib.auth import views as auth_views

app_name='account'

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # Fixed missing forward slash
    path('profile/', views.profile, name='profile'),  # Fixed missing forward slash
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # Fixed missing forward slash
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/uidb64/token/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]