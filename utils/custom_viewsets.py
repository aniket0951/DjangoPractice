from rest_framework import viewsets

from .custom_mixins import *

class ModelViewset(CreateModelMixin,
                   RetriveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   viewsets.GenericViewSet):

                   pass  