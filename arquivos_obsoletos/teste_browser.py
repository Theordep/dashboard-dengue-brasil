#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simulando requisições do navegador
"""

import requests
import json

def teste_como_navegador():
    print("TESTE SIMULANDO REQUISICOES DO NAVEGADOR")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api"
    
    # Headers simulando navegador
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Teste 1: Health Check
        print("1. Testando health check...")
        response = requests.get(f"{base_url}/health/", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        if response.status_code == 200:
            print("   OK")
        else:
            print(f"   ERRO: {response.text}")
        
        # Teste 2: Dashboard
        print("\n2. Testando dashboard...")
        response = requests.get(f"{base_url}/dashboard/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   OK - Total casos: {data.get('geral', {}).get('total_casos', 0):,}")
        else:
            print(f"   ERRO: {response.text}")
        
        # Teste 3: OPTIONS (preflight CORS)
        print("\n3. Testando OPTIONS (CORS preflight)...")
        response = requests.options(f"{base_url}/dashboard/", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers:")
        cors_headers = ['Access-Control-Allow-Origin', 'Access-Control-Allow-Methods', 'Access-Control-Allow-Headers']
        for header in cors_headers:
            if header in response.headers:
                print(f"     {header}: {response.headers[header]}")
        
        # Teste 4: POST carregar-estatisticas
        print("\n4. Testando POST carregar-estatisticas...")
        response = requests.post(f"{base_url}/carregar-estatisticas/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   OK - {data.get('total_registros', 0):,} registros")
        else:
            print(f"   ERRO: {response.text}")
        
        print("\n" + "=" * 50)
        print("TESTE CONCLUIDO!")
        print("=" * 50)
        
    except Exception as e:
        print(f"ERRO GERAL: {e}")

if __name__ == "__main__":
    teste_como_navegador()
