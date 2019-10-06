# from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer

User = get_user_model()

class UserViewSet(APIView) :

    def get_user(self, username) :

        try :
            found_user = User.objects.get(username=username)
            return found_user

        except User.DoesNotExist :
            return None

    def get(self, request, username, format=None) :

        found_user = self.get_user(username)

        if found_user is None :
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(found_user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)