from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import *
# from drama.models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'chat_%s' % self.room_name

        count = getattr(self.channel_layer, self.room_group_name, 0)
        if not count:
            setattr(self.channel_layer, self.room_group_name, 1)
        else:
            setattr(self.channel_layer, self.room_group_name, count + 1)
        print("join", self.channel_layer, self.room_group_name, count)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        count = getattr(self.channel_layer, self.room_group_name, 0)
        setattr(self.channel_layer, self.room_group_name, count - 1)
        if count == 1:
            delattr(self.channel_layer, self.room_group_name)
        print("Leave", count)
        print("Close Code :", close_code)
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        _type = text_data_json['type']
        print(_type)
        if _type == 'chat_message' :
            message = text_data_json['message']
            # sender = self.scope['session']['user_id']
            sender = self.user_name

            print("Receive message from WebSocket")

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender
                }
            )
        elif _type == 'count' :
            kind = text_data_json['kind']
            count = getattr(self.channel_layer, self.room_group_name + kind, 0)
            if not count:
                setattr(self.channel_layer, self.room_group_name + kind, 1)
            else:
                setattr(self.channel_layer, self.room_group_name + kind, count + 1)

            print(self.room_group_name, kind, count)

            if count % 10 == 0:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'kind': str(kind),
                        'message': str(kind) + str(count) + "개 돌파!",
                        'sender': 'AdminServer'
                    }
                )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = self.user_name
        if sender == 'AdminServer' :
            kind = event['kind']
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender,
                'kind': kind
            }))
        else :

            print("Receive message from room group", sender, receiver)

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender
            }))
