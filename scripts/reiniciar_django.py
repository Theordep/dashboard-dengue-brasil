#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para reiniciar o Django com as novas configurações
"""

import subprocess
import sys
import os
import time

def reiniciar_django():
    print("REINICIANDO SERVIDOR DJANGO...")
    print("=" * 40)
    
    # Mudar para o diretório backend
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    if not os.path.exists(backend_dir):
        print("ERRO: Diretorio backend nao encontrado!")
        return False
    
    try:
        print("1. Parando servidor Django (se estiver rodando)...")
        # Nota: Em produção, você usaria um processo manager como supervisor
        # Aqui vamos apenas iniciar o servidor
        
        print("2. Iniciando servidor Django com novas configurações...")
        print(f"   Diretorio: {backend_dir}")
        
        # Comando para iniciar o Django
        cmd = [sys.executable, 'manage.py', 'runserver']
        
        print("3. Executando comando:")
        print(f"   {' '.join(cmd)}")
        print()
        print("Para parar o servidor, pressione Ctrl+C")
        print("=" * 40)
        
        # Executar o comando
        subprocess.run(cmd, cwd=backend_dir)
        
        return True
        
    except KeyboardInterrupt:
        print("\nServidor Django parado pelo usuario.")
        return True
    except Exception as e:
        print(f"ERRO ao reiniciar Django: {e}")
        return False

if __name__ == "__main__":
    reiniciar_django()
