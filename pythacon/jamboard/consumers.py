import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

cood={'type':'init','data':[]}

class SketchConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'sketch'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps(cood))

    def receive(self, text_data):
        cood['data'].append(json.loads(text_data))
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'draw_message',
                'data':text_data
            }
        )
    
    def draw_message(self, event):
        self.send(text_data=event['data'])