#from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import User
# from drama.serializers import DramaSerializer

class UserSerializer(serializers.ModelSerializer):
    
    # dramas = DramaSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'profile_image']