from pyexpat import model
from rest_framework import serializers
from .models import User, Places

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User 
        fields = ['id', 'name', 'email', 'password', 'username']
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def create(self,validated_data):
        password = validated_data.pop('password', None) 
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance   

class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)        
        if instance.user:
            response['User'] = UserSerializer(instance.user).data
        return response    
