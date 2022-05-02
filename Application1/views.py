from django.shortcuts import render
from .models import User, Places
from .serializer import UserSerializer, PlacesSerializer
from rest_framework.decorators import action, api_view
from utils import custom_viewsets
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
from utils.utils import user_object
import http.client
import json
# Create your views here.


class UserViewSetAPIView(custom_viewsets.ModelViewset):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    create_success_message = 'User registration completed successfully!'
    list_success_message = 'User list returned successfully!'
    retrieve_success_message = 'Information returned successfully!'
    update_success_message = 'Information updated successfully!'

    data = {
        "data": None,
        "message": None,
    }


    @action(detail=False, methods=['POST'])
    def user_login(self, request):

        user = self.get_queryset().filter(id=14).first()
        serializer = self.get_serializer(user)
        payload = jwt_payload_handler(user)
        payload['username'] = user.name
        payload['id'] = user.id
        token = jwt_encode_handler(payload)
        expiration = datetime.utcnow(
        ) + settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
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
        # # user = user_object(request)
        user = User.objects.filter(name="aniket1").first()

        if not user:
            raise ValidationError("User not found !")

        serializer = self.get_serializer(user)
        self.data.update({"data": serializer.data,
                          "message": self.retrieve_success_message})

        data = dict()
        data['test1'] = "Aniket suryawanhsi from test 1"
        data['test'] =  "Aniket suryawanhsi from test"    

        mobile = str(user.mobile)
        send_message(mobile, "this is from testt mantra labs")            

        return Response(self.data, status=status.HTTP_200_OK)
@api_view(['GET'])    
def user_my_data(request):
    # data = User.objects.all()
    # serializer = UserSerializer(data, many=True)

    return Response("aniket", status=status.HTTP_200_OK)

class PlacesViewSetAPIView(custom_viewsets.ModelViewset):
    model = Places
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer

    create_success_message = 'Places added successfully!'
    list_success_message = 'Places list returned successfully!'
    retrieve_success_message = 'Places Information returned successfully!'
    update_success_message = 'Places Information updated successfully!'

    def get_permissions(self):
        if self.action in ['create', 'get_user_places']:
            permission_classes = [IsEndUser]
            return [permission() for permission in permission_classes]

        if self.action in ['whats_app_user']:
            permission_classes = [AllowAny]
            return [permission() for permission in permission_classes]

        if self.action == 'retrieve':
            permission_classes = [IsEndUser]
            return [permission() for permission in permission_classes]

        if self.action == 'list':
            permission_classes = [IsEndUser]
            return [permission() for permission in permission_classes]
        return super().get_permissions()

    @action(detail=False, methods=['GET'])
    def get_user_places(self, request):

        place_id = self.request.data.get('place_id')

        places = self.get_queryset().filter(id=place_id).first()

        if not places:
            raise ValidationError("Places not fond !")

        places.user.username = "Aniket Suryawanhsi"
        places.save()
        serializer = self.get_serializer(places)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def whats_app_user(self, request):
        mobile_number = self.request.data.get('mobile_number')
        message = self.request.data.get('message')

        data = send_message(mobile_number, message)

        # data['HTTPStatusCode'] == 200
        return Response(data, status=status.HTTP_200_OK)

def send_message(mobile_number, message):
        template_name = "web_guest_vcurl"
        sender = "916366442244"
        language = "en"

         

        authorization = 'App c3c6c881ee9ecc553da82d7b4ebbaedc-edaeb328-541a-4548-ac7b-f6f7c9d34e48'
        baseurl = "29y9z.api.infobip.com"
        conn = http.client.HTTPSConnection(f"{baseurl}")
        payload = json.dumps({
            "messages": [
                {
                    "from": f"{sender}",
                    "to": f"{mobile_number}",
                    "messageId": "a28dd97c-1ffb-4fcf-99f1-0b557ed381da",
                    "content": {
                        "templateName": f"{template_name}",
                        "templateData": {
                            "body": {
                                "placeholders": [
                                    f"{message}",
                                    "test",
                                    "test",
                                    "test"
                                ]
                            }
                        },
                        "language": f"{language}"
                    },
                    "callbackData": "Callback data",
                    "notifyUrl": "https://www.example.com/whatsapp"
                }
            ]
        })
        headers = {
            'Authorization': f'{authorization}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/whatsapp/1/message/template", payload, headers)
        res = conn.getresponse()
        data = res
        temp = data 
        data = json.load(temp)

        # data['HTTPStatusCode'] == 200
        return data
        return Response(data, status=status.HTTP_200_OK)

