import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

data={'type':'init','cood':[],'chat':[],'text':"",'lang':""}

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
        if(rdata['type']=='draw'):
            data['cood'].append(rdata)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'draw_message',
                    'data': text_data,
                    'user': self.scope["user"]
                }
            )
        if(rdata['type']=='chat'):
            data['chat'].append(rdata)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'data': text_data,
                    'user': self.scope["user"]
                }
            )
        if(rdata['type']=='edit'):
            data['text']=rdata
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'edit_message',
                    'data': text_data,
                    'user': self.scope["user"]
                }
            )
        if(rdata['type']=='lang-change'):
            data['lang']=rdata
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'lang_message',
                    'data': text_data,
                    'user': self.scope["user"]
                }
            )
        if(rdata['type']=='clear'):
            data['cood']=[]
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'clear_message',
                    'data': text_data,
                    'user': self.scope["user"]
                }
            )
    
    def draw_message(self, event):
        if self.scope["user"] != event['user']:
            self.send(text_data=event['data'])
    
    def chat_message(self, event):
        if self.scope["user"] != event['user']:
            self.send(text_data=event['data'])

    def edit_message(self, event):
        if self.scope["user"] != event['user']:
            self.send(text_data=event['data'])
    
    def lang_message(self, event):
        if self.scope["user"] != event['user']:
            self.send(text_data=event['data'])

    def clear_message(self, event):
        if self.scope["user"] != event['user']:
            self.send(text_data=event['data'])