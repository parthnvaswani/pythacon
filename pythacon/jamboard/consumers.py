import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

data={'type':'init','cood':[],'chat':[]}

class SketchConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'sketch'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps(data))

    def receive(self, text_data):
        rdata=json.loads(text_data)
        print(rdata)
        if(rdata['type']=='draw'):
            data['cood'].append(rdata)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'draw_message',
                    'data':text_data
                }
            )
        if(rdata['type']=='chat'):
            data['chat'].append(rdata)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'data':text_data
                }
            )
    
    def draw_message(self, event):
        self.send(text_data=event['data'])
    
    def chat_message(self, event):
        self.send(text_data=event['data'])