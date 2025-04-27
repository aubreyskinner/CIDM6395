from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import CNA, ClientProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CNASerializer(serializers.ModelSerializer):
    class Meta:
        model = CNA
        fields = '__all__'

class ClientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ClientProfile
        fields = '__all__'