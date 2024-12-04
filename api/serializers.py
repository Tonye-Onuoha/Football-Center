from rest_framework import serializers
from django.contrib.auth.models import User
from football.models import Comments, Profiles
        

class ProfilesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profiles
        fields = ['image', 'bio']
        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfilesSerializer()
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'profile']
        