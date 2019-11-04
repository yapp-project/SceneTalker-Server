# from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import status
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer
from drama.models import *

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


class AddDramaBookmark(APIView) :

    def post(self, request, drama_title, format=None) :

        user = request.user

        try :
            drama = Drama.objects.get(title=drama_title)
        except Drama.DoesNotExist :
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.drama_bookmark.add(drama)
        user.save()

        return Response(status=status.HTTP_200_OK)

class RemoveDramaBookmark(APIView) :

    def post(self, request, drama_title, format=None) :

        user = request.user

        try :
            drama = Drama.objects.get(title=drama_title)
        except Drama.DoesNotExist :
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.drama_bookmark.remove(drama)
        user.save()

        return Response(status=status.HTTP_200_OK)

class GetRealTimeUserBestDrama(APIView) :

    def get(self, request, format=None) :

        user = request.user

        user_drama_bookmarks = user.drama_bookmark.filter(is_broadcasiting=True).first()

        print(user_drama_bookmarks)

        return Response(status=status.HTTP_200_OK)

class PutUserProfileImage(APIView) :

    parser_classes = [MultiPartParser]

    def put(self, request, username, filename, format=None) :

        user = request.user

        file_obj = request.data['file']

        user.profile_image.save(filename, file_obj, save=True)
        return Response(status=status.HTTP_200_OK)