#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para CORS
"""

import requests

def teste_cors():
    print("TESTE ESPECIFICO DE CORS")
    print("=" * 30)
    
    base_url = "http://localhost:8000/api"
    
    # Headers simulando navegador com origin
    headers = {
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Content-Type',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Teste OPTIONS (preflight)
        print("1. Testando OPTIONS (CORS preflight)...")
        response = requests.options(f"{base_url}/dashboard/", headers=headers)
        
        print(f"   Status: {response.status_code}")
        print(f"   Headers de resposta:")
        
        # Verificar headers específicos de CORS
        cors_headers = {
            'Access-Control-Allow-Origin': 'Origem permitida',
            'Access-Control-Allow-Methods': 'Métodos permitidos',
            'Access-Control-Allow-Headers': 'Headers permitidos',
            'Access-Control-Allow-Credentials': 'Credenciais permitidas',
        }
        
        for header, desc in cors_headers.items():
            if header in response.headers:
                print(f"     {header}: {response.headers[header]}")
            else:
                print(f"     {header}: AUSENTE")
        
        # Teste GET com Origin
        print("\n2. Testando GET com Origin...")
        headers_get = {
            'Origin': 'http://localhost:3000',
            'Accept': 'application/json',
        }
        
        response = requests.get(f"{base_url}/dashboard/", headers=headers_get)
        print(f"   Status: {response.status_code}")
        
        if 'Access-Control-Allow-Origin' in response.headers:
            print(f"   Access-Control-Allow-Origin: {response.headers['Access-Control-Allow-Origin']}")
        else:
            print("   Access-Control-Allow-Origin: AUSENTE")
        
        print("\n" + "=" * 30)
        print("TESTE CORS CONCLUIDO!")
        print("=" * 30)
        
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    teste_cors()
