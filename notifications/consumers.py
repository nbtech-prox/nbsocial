import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"Tentativa de conexão WebSocket - Usuário autenticado: {not self.scope['user'].is_anonymous}")
        
        if self.scope["user"].is_anonymous:
            logger.info("Anonymous user tried to connect to notifications WebSocket.")
            await self.close()
        else:
            self.user = self.scope["user"]
            self.room_group_name = f'notifications_{self.user.id}'
            
            # Adicionar ao grupo de canal específico para o usuário
            logger.info(f"User {self.user.username} connected to notifications WebSocket. Path: {self.scope['path']}")
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            # Aceitar a conexão WebSocket
            await self.accept()
            
            # Enviar contagem de notificações não lidas ao conectar
            unread_count = await self.get_unread_notification_count()
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': unread_count
            }))
    
    async def disconnect(self, close_code):
        if hasattr(self, 'user') and hasattr(self, 'room_group_name'):
            logger.info(f"User {self.user.username} disconnected from notifications WebSocket.")
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            command = data.get('command')
            
            if command == 'mark_as_read':
                notification_id = data.get('notification_id')
                await self.mark_notification_as_read(notification_id)
                
                # Enviar contagem atualizada após marcar como lida
                unread_count = await self.get_unread_notification_count()
                await self.send(text_data=json.dumps({
                    'type': 'unread_count',
                    'count': unread_count
                }))
            elif command == 'mark_all_as_read':
                await self.mark_all_notifications_as_read()
                await self.send(text_data=json.dumps({
                    'type': 'unread_count',
                    'count': 0
                }))
            elif command == 'get_notifications':
                notifications = await self.get_recent_notifications(limit=data.get('limit', 10))
                await self.send(text_data=json.dumps({
                    'type': 'notifications_list',
                    'notifications': notifications
                }))
        except json.JSONDecodeError:
            logger.error("Invalid JSON received in WebSocket message")
        except Exception as e:
            logger.error(f"Error in WebSocket receive: {str(e)}")
    
    async def notification(self, event):
        """Envia notificação para o cliente WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))
    
    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        """Marca uma notificação específica como lida"""
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient=self.user,
                read=False
            )
            notification.read = True
            notification.save(update_fields=['read'])
            return True
        except Notification.DoesNotExist:
            logger.warning(f"Notification {notification_id} not found or already read")
            return False
    
    @database_sync_to_async
    def mark_all_notifications_as_read(self):
        """Marca todas as notificações do usuário como lidas"""
        return Notification.objects.filter(
            recipient=self.user,
            read=False
        ).update(read=True)
    
    @database_sync_to_async
    def get_unread_notification_count(self):
        """Retorna o número de notificações não lidas"""
        return Notification.objects.filter(
            recipient=self.user,
            read=False
        ).count()
    
    @database_sync_to_async
    def get_recent_notifications(self, limit=10):
        """Retorna as notificações mais recentes do usuário"""
        notifications = Notification.objects.filter(
            recipient=self.user
        ).order_by('-created_at')[:limit]
        
        # Converter para lista de dicionários para serialização JSON
        return [
            {
                'id': notification.id,
                'sender': notification.sender.username,
                'type': notification.notification_type,
                'read': notification.read,
                'created_at': notification.created_at.isoformat(),
                'content': notification.get_notification_text(),
                'url': notification.get_notification_url(),
            } 
            for notification in notifications
        ]
