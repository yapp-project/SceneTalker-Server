from rest_framework import serializers
from .models import User
from drama.models import DramaSerializer

class UserSerializer(serializers.ModelSerializer):
    
    drama_bookmark = DramaSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'profile_image', 'drama_bookmark']