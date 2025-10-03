#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a integração completa do sistema
"""

import requests
import json
import time

def test_api():
    """
    Testa os endpoints da API
    """
    base_url = "http://localhost:8000/api"
    
    print("🧪 TESTANDO INTEGRAÇÃO COMPLETA DO SISTEMA")
    print("=" * 60)
    
    # Teste 1: Health Check
    print("\n1️⃣ Testando Health Check...")
    try:
        response = requests.get(f"{base_url}/health/", timeout=10)
        if response.status_code == 200:
            print("✅ Health Check: OK")
            print(f"   Resposta: {response.json()}")
        else:
            print(f"❌ Health Check: Erro {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check: {e}")
    
    # Teste 2: Carregar Estatísticas
    print("\n2️⃣ Carregando estatísticas...")
    try:
        response = requests.post(f"{base_url}/carregar-estatisticas/", timeout=30)
        if response.status_code == 200:
            print("✅ Estatísticas carregadas com sucesso!")
            data = response.json()
            print(f"   Total de registros: {data.get('total_registros', 'N/A'):,}")
        else:
            print(f"❌ Erro ao carregar estatísticas: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao carregar estatísticas: {e}")
    
    # Teste 3: Dashboard Overview
    print("\n3️⃣ Testando Dashboard Overview...")
    try:
        response = requests.get(f"{base_url}/dashboard/", timeout=15)
        if response.status_code == 200:
            print("✅ Dashboard Overview: OK")
            data = response.json()
            print(f"   Total de casos: {data.get('geral', {}).get('total_casos', 'N/A'):,}")
            print(f"   Estados únicos: {data.get('geral', {}).get('estados_unicos', 'N/A')}")
        else:
            print(f"❌ Dashboard Overview: Erro {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard Overview: {e}")
    
    # Teste 4: Estatísticas por Estado
    print("\n4️⃣ Testando Estatísticas por Estado...")
    try:
        response = requests.get(f"{base_url}/estados/", timeout=15)
        if response.status_code == 200:
            print("✅ Estatísticas por Estado: OK")
            data = response.json()
            print(f"   Estados analisados: {len(data.get('estados', []))}")
        else:
            print(f"❌ Estatísticas por Estado: Erro {response.status_code}")
    except Exception as e:
        print(f"❌ Estatísticas por Estado: {e}")
    
    # Teste 5: Sintomas
    print("\n5️⃣ Testando Sintomas...")
    try:
        response = requests.get(f"{base_url}/sintomas/", timeout=15)
        if response.status_code == 200:
            print("✅ Sintomas: OK")
            data = response.json()
            print(f"   Sintomas analisados: {len(data.get('sintomas', []))}")
        else:
            print(f"❌ Sintomas: Erro {response.status_code}")
    except Exception as e:
        print(f"❌ Sintomas: {e}")
    
    # Teste 6: Santa Catarina
    print("\n6️⃣ Testando Santa Catarina...")
    try:
        response = requests.get(f"{base_url}/santa-catarina/", timeout=15)
        if response.status_code == 200:
            print("✅ Santa Catarina: OK")
            data = response.json()
            print(f"   Casos em SC: {data.get('total_casos', 0):,}")
            print(f"   Criciúma: {data.get('criciuma', {}).get('casos', 0)} casos")
        else:
            print(f"❌ Santa Catarina: Erro {response.status_code}")
    except Exception as e:
        print(f"❌ Santa Catarina: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 TESTE DE INTEGRAÇÃO CONCLUÍDO!")
    print("=" * 60)
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Iniciar o servidor Django: cd backend && python manage.py runserver")
    print("2. Iniciar o React: cd frontend && npm start")
    print("3. Acessar: http://localhost:3000")
    print("4. Verificar se todos os dados estão sendo exibidos corretamente")

def main():
    test_api()

if __name__ == "__main__":
    main()
