#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar o processador avançado de dados de dengue
"""

from data_processor_advanced import DengueAdvancedProcessor
import os
import sys

def main():
    print("=" * 80)
    print("PROCESSADOR AVANÇADO DE DADOS DE DENGUE")
    print("=" * 80)
    
    # Verificar se o arquivo CSV existe
    csv_path = 'Documentos/DENGBR25.csv'
    
    if not os.path.exists(csv_path):
        print(f"Erro: O arquivo {csv_path} não foi encontrado.")
        print("Por favor, certifique-se de que o arquivo CSV está no diretório atual.")
        return False
    
    # Criar e executar o processador avançado
    try:
        processor = DengueAdvancedProcessor(csv_path)
        success = processor.process_all()
        
        if success:
            print("\nPROCESSAMENTO AVANÇADO CONCLUÍDO COM SUCESSO!")
            print("=" * 80)
            print("\nPróximos passos:")
            print("1. Execute o servidor Django (python manage.py runserver)")
            print("2. Acesse a API em http://localhost:8000/api/avancado/carregar-estatisticas/ para carregar os dados")
            print("3. Acesse a página de Análise Avançada no frontend")
            return True
        else:
            print("\nERRO: O processamento avançado não foi concluído.")
            return False
            
    except Exception as e:
        print(f"\nERRO: Ocorreu uma exceção durante o processamento: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
