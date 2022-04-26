import re
from Application1.models import User
from rest_framework import exceptions

def user_object(request):
    try:
        if request.user and request.user.id:
            return User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed("Invalid user found !")    
