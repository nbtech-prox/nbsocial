#!/usr/bin/env python
"""
Script para iniciar o servidor ASGI com suporte a WebSockets e arquivos estáticos/mídia
"""
import os
import django
import uvicorn

# Configurar variáveis de ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nbsocial.settings')
django.setup()

# Verificar caminhos dos arquivos estáticos e de mídia
from django.conf import settings
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")

if __name__ == "__main__":
    print("Iniciando servidor ASGI com suporte a WebSockets...")
    print("Acesse: http://127.0.0.1:8000")
    print("WebSocket disponível em: ws://127.0.0.1:8000/ws/notifications/")
    
    uvicorn.run(
        "nbsocial.asgi_dev:application",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
