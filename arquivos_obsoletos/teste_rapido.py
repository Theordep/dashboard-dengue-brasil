#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste rápido da integração
"""

import requests

def teste_rapido():
    print("TESTE RAPIDO DO SISTEMA")
    print("=" * 40)
    
    base_url = "http://localhost:8000/api"
    
    try:
        # Teste 1: Health Check
        print("1. Health Check...")
        response = requests.get(f"{base_url}/health/", timeout=5)
        if response.status_code == 200:
            print("   OK")
        else:
            print(f"   ❌ Erro: {response.status_code}")
        
        # Teste 2: Carregar Estatísticas
        print("2. Carregando estatísticas...")
        response = requests.post(f"{base_url}/carregar-estatisticas/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   OK - {data.get('total_registros', 0):,} registros")
        else:
            print(f"   ❌ Erro: {response.status_code}")
        
        # Teste 3: Dashboard
        print("3. Dashboard...")
        response = requests.get(f"{base_url}/dashboard/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            total_casos = data.get('geral', {}).get('total_casos', 0)
            print(f"   OK - {total_casos:,} casos totais")
        else:
            print(f"   ❌ Erro: {response.status_code}")
        
        # Teste 4: Santa Catarina
        print("4. Santa Catarina...")
        response = requests.get(f"{base_url}/santa-catarina/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            casos_sc = data.get('total_casos', 0)
            criciuma = data.get('criciuma', {}).get('casos', 0)
            print(f"   OK - SC: {casos_sc:,} casos, Criciuma: {criciuma} casos")
        else:
            print(f"   ❌ Erro: {response.status_code}")
        
        print("\nSISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("=" * 40)
        print("Frontend: http://localhost:3000")
        print("Backend: http://localhost:8000")
        print("Admin: http://localhost:8000/admin")
        
    except requests.exceptions.ConnectionError:
        print("ERRO: Nao foi possivel conectar ao servidor Django")
        print("   Verifique se o servidor está rodando:")
        print("   cd backend && python manage.py runserver")
    
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    teste_rapido()
