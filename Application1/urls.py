from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSetAPIView, PlacesViewSetAPIView, user_my_data

router = DefaultRouter(trailing_slash=False)

router.register('user', UserViewSetAPIView)
router.register('places', PlacesViewSetAPIView)

urlpatterns = [
    path('user_my_data', user_my_data),
    * router.urls
]
