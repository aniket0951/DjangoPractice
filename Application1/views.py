from django.shortcuts import render
from .models import User, Places
from .serializer import UserSerializer, PlacesSerializer
from rest_framework.decorators import action
from utils import  custom_viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class UserViewSetAPIView(custom_viewsets.ModelViewset):
    model = User 
    queryset = User.objects.all()
    serializer_class = UserSerializer

    create_success_message = 'User registration completed successfully!'
    list_success_message = 'User list returned successfully!'
    retrieve_success_message = 'Information returned successfully!'
    update_success_message = 'Information updated successfully!'

    @action(detail=False, methods=['POST'])
    def user_login(self, request):
        return Response(self.create_success_message, status=status.HTTP_200_OK)
        pass

class UserModelViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PlacesViewSetAPIView(custom_viewsets.ModelViewset):
    model = Places
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer

    create_success_message = 'Places added successfully!'
    list_success_message = 'Places list returned successfully!'
    retrieve_success_message = 'Places Information returned successfully!'
    update_success_message = 'Places Information updated successfully!'

