#!/usr/bin/env python
"""
Script para iniciar o servidor ASGI com Daphne
"""
import os
import subprocess
import sys

# Caminho para o Python no ambiente virtual
PYTHON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv/bin/python')

if __name__ == "__main__":
    print("Iniciando servidor Daphne com suporte a WebSockets...")
    print("Acesse: http://127.0.0.1:8000")
    print("WebSocket disponível em: ws://127.0.0.1:8000/ws/notifications/")
    
    # Executar o Daphne
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nbsocial.settings')
    subprocess.run([PYTHON_PATH, "-m", "daphne", "nbsocial.asgi:application"])
