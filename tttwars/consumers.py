import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket (Sending Messages)
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'message' in text_data_json:
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {'type': 'chat_message', 'message': text_data_json['message'], 'username': text_data_json['username']}
            )
        elif 'join' in text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {'type': 'join'}
            )
        elif 'resign' in text_data_json:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {'type': 'resign'}
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    'type': 'move_info', 'newsquare': text_data_json['newsquare'], 'id': text_data_json['id'],
                    'reload': text_data_json['reload'], 'p1totalscore': text_data_json['p1totalscore'], 'p2totalscore': text_data_json['p2totalscore'],
                    'p1score': text_data_json['p1score'], 'p2score': text_data_json['p2score']
                })

    # Receive message from room group (Receiving Messages)
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({'message': message, 'username': event['username']}))

    def move_info(self, event):
        newsquare = event['newsquare']
        id = event['id']
        reload = event['reload']
        p1totalscore = event['p1totalscore']
        p2totalscore = event['p2totalscore']
        p1score = event['p1score']
        p2score = event['p2score']

        # Send move to Websocket
        self.send(text_data=json.dumps({
            'newsquare': newsquare, 'id': id, 'reload': reload,
            'p1totalscore': p1totalscore, 'p2totalscore': p2totalscore,
            'p1score': p1score, 'p2score': p2score
            }))

    def join(self, event):
        self.send(text_data=json.dumps({'join': 'True'}))

    def resign(self, event):
        self.send(text_data=json.dumps({'resign': 'True'}))
