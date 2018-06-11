import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ApplicationNotificationsConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_id = None
        self.app_group_name = None

    async def connect(self):
        self.app_id = self.scope['url_route']['kwargs']['id']
        self.app_group_name = 'app_{}'.format(self.app_id)

        await self.channel_layer.group_add(
            self.app_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.app_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
