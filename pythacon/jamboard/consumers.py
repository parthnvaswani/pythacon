import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

rooms={}

class SketchConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room']

        if self.room_group_name not in rooms.keys():
            rooms[self.room_group_name] = {'owner': self.scope['user'].username,
                                           'type': 'init', 'cood': [], 'chat': [], 'text': "", 'lang': ""}

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps(rooms[self.room_group_name]))

    def receive(self, text_data):
        rdata=json.loads(text_data)
        if(rdata['type']=='draw'):
            rooms[self.room_group_name]['cood'].append(rdata)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'draw_message',
                    'data': text_data,
                    'user': self.scope["user"]
                }
            )
        if(rdata['type']=='chat'):
            rdata['user'] = self.scope['user'].username
            rooms[self.room_group_name]['chat'].append(rdata)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'data': json.dumps(rdata),
                    'user': self.scope["user"]
                }
            )
        if(rdata['type']=='edit'):
            rooms[self.room_group_name]['text'] = rdata
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'edit_message',
                    'data': text_data,
                    'user': self.scope["user"]
                }
            )
        if(rdata['type']=='lang-change'):
            rooms[self.room_group_name]['lang'] = rdata
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'lang_message',
                    'data': text_data,
                    'user': self.scope["user"]
                }
            )
        if(rdata['type']=='clear'):
            rooms[self.room_group_name]['cood'] = []
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'clear_message',
                    'data': text_data,
                    'user': self.scope["user"]
                }
            )
        if(rdata['type']=='end'):
            if self.scope['user'].username == rooms[self.room_group_name]['owner']:
                del rooms[self.room_group_name]
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'del_message',
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

    def del_message(self, event):
        self.send(text_data=json.dumps({'type': 'room deleted'}))
