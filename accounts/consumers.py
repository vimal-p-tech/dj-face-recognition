import cv2
import base64

from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import asyncio
class CameraFeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.loop = asyncio.get_running_loop()
        self.cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            self.send(frame_bytes)
            asyncio.sleep(0.1)
        
    async def disconnect(self):
        pass