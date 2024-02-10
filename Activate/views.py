#https://stackoverflow.com/questions/47154404/djoser-user-activation-email-post-example
# yourappname/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Import status codes
import requests
from django.shortcuts import render
from django.conf import settings

class UserActivationView(APIView):
    def get (self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        print(post_url)
        print(post_url)
        result = requests.post(post_url, data = post_data)

        if result.status_code == status.HTTP_204_NO_CONTENT:
            return render(request, 'activation_success.html', {'detail': 'Your account has been successfully activated!'})
        elif result.status_code == status.HTTP_400_BAD_REQUEST:
            return render(request, 'activation_error.html', {'detail': 'Invalid uid or token'})
        elif result.status_code == status.HTTP_403_FORBIDDEN:
            return render(request, 'activation_error.html', {'detail': 'User is already active'})
        else:
            # Handle other status codes if needed
            return render(request, 'activation_error.html', {'detail': 'Activation failed'})


class PasswordResetConfirmView(APIView):
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        re_new_password = request.data.get('re_new_password')

        # Check if uid, token, and new_password are present in the request data
        if not uid or not token or not new_password:
            return render(request, 'password_reset_confirm_error.html', {'detail': 'uid, token, and new_password are required'})

        # Check if re_new_password is required and present
        if settings.PASSWORD_RESET_CONFIRM_RETYPE and not re_new_password:
            return render(request, 'password_reset_confirm_error.html', {'detail': 're_new_password is required'})

        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/users/reset_password_confirm/"
        post_data = {'uid': uid, 'token': token, 'new_password': new_password, 're_new_password': re_new_password}

        # Make the POST request to confirm password reset
        result = requests.post(post_url, data=post_data)

        # Check the response status code and render appropriate HTML page
        if result.status_code == status.HTTP_204_NO_CONTENT:
            return render(request, 'password_reset_confirm_success.html', {'detail': 'Password reset successful!'})
        elif result.status_code == status.HTTP_400_BAD_REQUEST:
            return render(request, 'password_reset_confirm_error.html', {'detail': 'Invalid uid, token, or new_password'})
        else:
            # Handle other status codes if needed
            return render(request, 'password_reset_confirm_error.html', {'detail': 'Password reset failed'})