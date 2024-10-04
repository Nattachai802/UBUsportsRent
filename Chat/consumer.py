# consumer.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer): #คลาสนี้สืบทอดมาจาก AsyncWebsocketConsumer ซึ่งเป็นคลาสของ Django Channels
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] #ดึงค่าชื่อห้องจาก URL ที่ส่งมาในคำขอ WebSocket โดย room_name มาจาก URL ที่กำหนดใน routing.py
        self.room_group_name = f'chat_{self.room_name}'#สร้างชื่อกลุ่มห้องแชทที่ไม่ซ้ำกันด้วยการต่อข้อความ 'chat_' กับชื่อห้อง (room_name) 

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )#ให้ผู้ใช้เข้าร่วมใน room_group_name ที่อ้างอิงโดย channel_layer โดย channel_name คือช่องทางเฉพาะของการเชื่อมต่อของผู้ใช้คนนี้

        await self.accept() #ยอมรับการเชื่อมต่อ WebSocket โดยเมื่อเรียกคำสั่งนี้ WebSocket จะเปิดให้ผู้ใช้สามารถส่งและรับข้อความได้

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )#นำผู้ใช้ออกจากกลุ่มแชทที่เกี่ยวข้อง

    # Receive message from WebSocket
    async def receive(self, text_data): #เมื่อมีข้อความใหม่ที่ถูกส่งมาจากฝั่งผู้ใช้ผ่าน WebSocket
        text_data_json = json.loads(text_data) #แปลงJSON เป็น dictionary             
        message = text_data_json['message'] #ดึงข้อความ
        username = text_data_json['username'] #ดึงusername

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )#งข้อความไปที่ room_group_name โดยส่งข้อมูลที่มี type เป็น 'chat_message'

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message'] #รับข้อความจากอีเวนต์
        username = event['username'] #รับชื่อผู้ใช้จากอีเวนต์

        # Send message to WebSocket
        await self.send(text_data=json.dumps({ #ส่งข้อความไปยัง WebSocket ของผู้ใช้ โดยแปลงข้อมูล message และ username เป็น JSON string ก่อนส่ง
            'message': message,
            'username': username
        }))
