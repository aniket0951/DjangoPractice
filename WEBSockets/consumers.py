from channels.generic.websocket import WebsocketConsumer
import json 
from Application1.models import User
from Application1.serializer import UserSerializer

class MyWebSocketConsumer(WebsocketConsumer):
    def connect(self):
        print('Websocket Connected ....')
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        user_id = data['id']
        name = data['name']
        user = User.objects.filter(id=user_id).first()
        user.name = name
        user.save()

        new_user = User.objects.all()
        serializer = UserSerializer(new_user, many=True)
        user_data = serializer.data
        print()
        self.send(text_data=json.dumps({"user_data":user_data}))

    def disconnect(self, close_code=None):
        print('Disconnect ....', close_code)      