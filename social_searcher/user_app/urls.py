from django.urls import path, re_path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('sign_up/', SignUpView.as_view()),
    path('profile/', UserProfile.as_view()),
    path('confirm_email/', ConfirmEmailView.as_view(), name='confirm_email'),
    re_path(r'^confirm_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         ConfirmEmailView.as_view(), name='confirm_email'),
    path('vk_auth/', VKAuth.as_view(), name='vk-auth')
]
