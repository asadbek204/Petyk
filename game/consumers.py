import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import RequestAborted
from user.serializers import UserSerializer, User
from channels.db import database_sync_to_async


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.first = True
        await self.accept()

    async def disconnect(self, close_code):
        ...

    async def receive(self, text_data):
        if self.first:
            self.id = int(text_data)
            user = await self.get_user()
            self.first = False
            return
        print(text_data)
        user: User = await self.get_user()
        if text_data == 'inc_balance':
            if user.energy - user.tap_step <= 0:
                user.balance += user.energy
                user.energy = 0
            elif user.energy >= 0:
                user.balance += user.tap_step
                user.energy -= user.tap_step
        elif text_data != 'get_info':
            raise RequestAborted()
        await self.send(text_data=json.dumps(await self.save(user)))
    
    @database_sync_to_async
    def save(self, user: User):
        user.save()
        return UserSerializer(user).data

    @database_sync_to_async
    def get_user(self) -> User:
        try:
            user = User.objects.get(user_id=self.id)
        except User.DoesNotExist:
            raise RequestAborted()
        return user
