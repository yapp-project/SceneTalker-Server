from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.http import JsonResponse
from channels.layers import get_channel_layer

# Create your views here.
def room(request, room_name, user_name):

    current_user = user_name

    context = {
                'room_name_json' : mark_safe(json.dumps(room_name)), 
                'current_user_name_json' : mark_safe(json.dumps(current_user)),
                'current_user' : current_user 
                }

    return render(request, 'chat/room.html', context)
