#https://stackoverflow.com/questions/47154404/djoser-user-activation-email-post-example
# yourappname/urls.py
from django.urls import path
from .views import UserActivationView, PasswordResetConfirmView

urlpatterns = [
    path('activate/<str:uid>/<str:token>/', UserActivationView.as_view(), name='activate_user'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
