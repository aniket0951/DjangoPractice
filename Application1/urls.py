from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSetAPIView, UserModelViewset, PlacesViewSetAPIView

router = DefaultRouter(trailing_slash=False)

router.register('user', UserViewSetAPIView)
router.register('user_model', UserModelViewset)
router.register('places', PlacesViewSetAPIView)

urlpatterns = [
    * router.urls
]
