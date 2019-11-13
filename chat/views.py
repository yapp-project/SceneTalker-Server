from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.http import JsonResponse
from channels.layers import get_channel_layer
from rest_framework.views import APIView
from drama.models import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def room(request, room_name, user_name):

    current_user = user_name

    context = {
                'room_name_json' : mark_safe(json.dumps(room_name)), 
                'current_user_name_json' : mark_safe(json.dumps(current_user)),
                'current_user' : current_user 
                }

    return render(request, 'chat/room.html', context)

class GetDramaEachEpisodeCount(APIView) :

    def get(self, request, drama_id, episode, format=None) :
        try :
            drama_each_episode = DramaEachEpisode.objects.get(drama__id=drama_id, episode=episode)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DramaEachEpisodeSerializer(drama_each_episode)

        return Response(data=serializer.data, status=status.HTTP_200_OK)