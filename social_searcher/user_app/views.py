from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from rest_framework.permissions import IsAuthenticated
import requests
from django.urls import reverse
from django.conf import settings


class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfile(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ConfirmEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response('Thank you for your email confirmation. Now you can login your account.')

        return Response('Activation link is invalid!')


class VKAuth(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'error': 'No code provided'})

        response = requests.get(
            'https://oauth.vk.com/access_token',
            {
                'client_id': settings.VK_CLIENT_ID,
                'client_secret': settings.VK_CLIENT_SECRET,
                'redirect_uri': 'http://social-search.s3-website.eu-central-1.amazonaws.com/user',
                'code': code
            }
        )
        # reverse('vk-auth')
        response = response.json()
        access_token = response.get('access_token')

        if not access_token:
            return Response({'error': 'VK authentication error'})

        request.user.vk_token = access_token
        request.user.save()

        return Response('OK')
