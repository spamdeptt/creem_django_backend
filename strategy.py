# Created because it was instructed by https://medium.com/@stevelukis/google-oauth2-with-django-and-react-f64d0a487bbb

from rest_framework.authtoken.models import Token

class TokenStrategy:
    @classmethod
    def obtain(cls, user):
        token, _ = Token.objects.get_or_create(user=user)

        return {
            "access": str(token),
        }