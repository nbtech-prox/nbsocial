"""
ASGI config para desenvolvimento que serve arquivos estáticos e de mídia
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from whitenoise.middleware import WhiteNoiseMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nbsocial.settings')
django.setup()

# Importar depois de configurar o Django
from notifications.routing import websocket_urlpatterns

# Classe para servir arquivos estáticos e de mídia
class StaticFilesASGIApplication:
    """
    ASGI application that serves static and media files 
    """
    def __init__(self, app):
        self.whitenoise = WhiteNoiseMiddleware(app)
        self.app = app
    
    async def __call__(self, scope, receive, send):
        path = scope.get('path', '')
        
        # Servir arquivos estáticos via whitenoise
        if path.startswith('/static/'):
            await self.whitenoise(scope, receive, send)
            return
            
        # Servir arquivos de mídia
        if path.startswith('/media/'):
            # Modifica o path para apontar para o diretório de mídia
            media_path = os.path.join(settings.MEDIA_ROOT, path[7:])
            if os.path.exists(media_path) and not os.path.isdir(media_path):
                with open(media_path, 'rb') as f:
                    content = f.read()
                
                await send({
                    'type': 'http.response.start',
                    'status': 200,
                    'headers': [
                        [b'content-type', b'application/octet-stream'],
                        [b'content-length', str(len(content)).encode()],
                    ]
                })
                await send({
                    'type': 'http.response.body',
                    'body': content,
                    'more_body': False
                })
                return
        
        # Passa para a aplicação principal
        await self.app(scope, receive, send)

# Aplicação ASGI principal
application = ProtocolTypeRouter({
    "http": StaticFilesASGIApplication(get_asgi_application()),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
