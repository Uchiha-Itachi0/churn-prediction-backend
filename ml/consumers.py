from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

logger = logging.getLogger(__name__)


class TrainingProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.model_id = self.scope['url_route']['kwargs']['model_id']
        self.group_name = f"training_{self.model_id}"

        logger.info(f"WebSocket connecting for model_id: {self.model_id}")

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        logger.info(f"WebSocket connected and joined group: {self.group_name}")
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnecting for model_id: {self.model_id}")
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def training_progress(self, event):
        logger.info(f"Sending progress update for model_id {self.model_id}: {event['progress']}%")
        await self.send(text_data=json.dumps({
            'progress': event['progress']
        }))