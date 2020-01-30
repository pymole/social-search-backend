from .views import *
from django.urls import path


urlpatterns = [
    path('', MethodView.as_view()),
]
