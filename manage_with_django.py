#!/usr/bin/env python
"""
Script para iniciar o servidor Django com suporte a WebSockets usando runserver
"""
import os
import sys
import django

if __name__ == "__main__":
    # Configurar variáveis de ambiente
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nbsocial.settings')
    
    # Inicializar Django
    django.setup()
    
    # Importar after_setup para evitar erro circular
    from django.core.management import execute_from_command_line
    
    # Avisos
    print("Iniciando servidor Django com suporte a WebSockets...")
    print("Acesse: http://127.0.0.1:8000")
    
    # Iniciar o servidor
    execute_from_command_line(['manage.py', 'runserver'])
