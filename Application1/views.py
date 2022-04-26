from django.shortcuts import render
from .models import User, Places
from .serializer import UserSerializer, PlacesSerializer
from rest_framework.decorators import action
from utils import  custom_viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.validators import ValidationError
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler
from datetime import datetime
from django.conf import settings
from utils.custom_jwt_authentication import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.custome_permissions import IsEndUser

# Create your views here.
class UserViewSetAPIView(custom_viewsets.ModelViewset):
    model = User 
    queryset = User.objects.all()
    serializer_class = UserSerializer

    create_success_message = 'User registration completed successfully!'
    list_success_message = 'User list returned successfully!'
    retrieve_success_message = 'Information returned successfully!'
    update_success_message = 'Information updated successfully!'

    data = {
        "data": None,
        "message": None,
    }

    def get_permissions(self):
        if self.action in ['create', 'user_login']:
            permission_classes = [AllowAny]
            return [permission() for permission in permission_classes]

        if self.action in ['user_data']:
            permission_classes = [IsEndUser]
            return [permission() for permission in permission_classes]

        if self.action == 'retrieve':
            permission_classes = [IsEndUser]
            return [permission() for permission in permission_classes]

        if self.action == 'list':
            permission_classes = [IsEndUser]
            return [permission() for permission in permission_classes]    
        return super().get_permissions()

    @action(detail=False, methods=['POST'])
    def user_login(self, request):

        user = self.get_queryset().filter(id=1).first()
        serializer = self.get_serializer(user)
        payload = jwt_payload_handler(user)
        payload['username'] = user.name
        payload['id'] = user.id
        token = jwt_encode_handler(payload)
        expiration = datetime.utcnow() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
        expiration_epoch = expiration.timestamp()

        WhiteListedJWTTokenUtil.create_token(user, token)

        data = {
            "data": serializer.data,
            "message": "token saved successfully",
            "token": token,
            "token_expiration": expiration_epoch
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET']) 
    def user_data(self, request):
        user_id = self.request.data.get('user_id')

        if not user_id:
            raise ValidationError("Provide a params !")

        user = self.get_queryset().filter(id=user_id).first()

        if not user:
            raise ValidationError("User not found !")

        serializer = self.get_serializer(user) 
        self.data.update({"data": serializer.data,
                          "message": self.retrieve_success_message})

        return Response(self.data, status=status.HTTP_200_OK)                         



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

    @action(detail=False, methods=['GET'])
    def get_user_places(self,request):

        place_id = self.request.data.get('place_id')

        places = self.get_queryset().filter(id=place_id).first()
        
        if not places:
            raise ValidationError("Places not fond !")
        
        # serializer = PlacesSerializer(places)
        serializer = self.get_serializer(places)
        return Response(serializer.data,status=status.HTTP_200_OK)    
