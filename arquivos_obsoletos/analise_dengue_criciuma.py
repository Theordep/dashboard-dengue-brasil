#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise de Dados de Dengue - Criciúma/SC
Trabalho de Estatística Aplicada com Python e Pandas

Autor: Estudante de Engenharia de Software
Data: 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuração para exibir gráficos em português
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

def carregar_dados():
    """
    Carrega os dados do arquivo CSV do DATASUS
    """
    print("Carregando dados do DENGBR25.csv...")
    
    try:
        # Carregar apenas as primeiras 1000 linhas para teste inicial
        df = pd.read_csv('Documentos/DENGBR25.csv', nrows=1000, low_memory=False)
        print(f"Dados carregados com sucesso! Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None

def explorar_dados(df):
    """
    Explora a estrutura e conteúdo dos dados
    """
    print("\nEXPLORACAO INICIAL DOS DADOS")
    print("=" * 50)
    
    # Informações gerais
    print(f"Dimensoes do dataset: {df.shape[0]} linhas x {df.shape[1]} colunas")
    
    # Colunas disponíveis
    print(f"\nColunas disponiveis ({len(df.columns)}):")
    for i, col in enumerate(df.columns):
        print(f"  {i+1:2d}. {col}")
    
    # Primeiras linhas
    print(f"\nPrimeiras 5 linhas:")
    print(df.head())
    
    # Informações sobre tipos de dados
    print(f"\nTipos de dados:")
    print(df.dtypes.value_counts())
    
    # Verificar valores únicos em colunas importantes
    colunas_interesse = ['SG_UF_NOT', 'ID_MUNICIP', 'MUNICIPIO', 'CS_SEXO', 'CLASSI_FIN']
    for col in colunas_interesse:
        if col in df.columns:
            print(f"\nValores unicos em {col}: {df[col].nunique()}")
            if df[col].nunique() <= 20:
                print(f"   Valores: {df[col].unique()}")

def identificar_criciuma(df):
    """
    Identifica dados específicos de Criciúma no dataset
    """
    print("\nIDENTIFICANDO DADOS DE CRICIÚMA")
    print("=" * 50)
    
    # Criciúma tem código IBGE 4204608
    # Vamos procurar por diferentes formas de identificar Criciúma
    
    # Buscar por código do município
    if 'ID_MUNICIP' in df.columns:
        codigos_criciuma = df[df['ID_MUNICIP'] == '4204608']
        print(f"Casos encontrados com codigo ID_MUNICIP 4204608: {len(codigos_criciuma)}")
    
    # Buscar por nome do município
    if 'MUNICIPIO' in df.columns:
        criciuma_nome = df[df['MUNICIPIO'].str.contains('CRICIÚMA', case=False, na=False)]
        print(f"Casos encontrados com nome 'CRICIÚMA': {len(criciuma_nome)}")
        
        # Verificar variações do nome
        print(f"Variacoes do nome encontradas:")
        nomes_unicos = df['MUNICIPIO'].str.upper().str.contains('CRICI', na=False)
        if nomes_unicos.any():
            print(f"   Municipios com 'CRICI': {df[nomes_unicos]['MUNICIPIO'].unique()}")
    
    # Buscar em Santa Catarina (UF 42)
    if 'SG_UF_NOT' in df.columns:
        sc_casos = df[df['SG_UF_NOT'] == '42']
        print(f"Total de casos em Santa Catarina: {len(sc_casos)}")
        
        if 'MUNICIPIO' in sc_casos.columns:
            municipios_sc = sc_casos['MUNICIPIO'].value_counts().head(10)
            print(f"Top 10 municipios de SC com mais casos:")
            for municipio, casos in municipios_sc.items():
                print(f"   {municipio}: {casos} casos")

def analisar_casos_por_periodo(df):
    """
    Analisa casos por período temporal
    """
    print("\nANALISE TEMPORAL DOS CASOS")
    print("=" * 50)
    
    if 'DT_NOTIFIC' in df.columns:
        # Converter data
        df['DT_NOTIFIC'] = pd.to_datetime(df['DT_NOTIFIC'], errors='coerce')
        
        # Casos por mês
        df['MES'] = df['DT_NOTIFIC'].dt.month
        df['ANO'] = df['DT_NOTIFIC'].dt.year
        
        casos_mes = df.groupby(['ANO', 'MES']).size()
        print(f"Casos por mes/ano:")
        print(casos_mes.head(10))
        
        # Plotar evolução temporal
        plt.figure(figsize=(12, 6))
        casos_mes.plot(kind='line', marker='o')
        plt.title('Evolução dos Casos de Dengue por Mês')
        plt.xlabel('Período')
        plt.ylabel('Número de Casos')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('evolucao_casos_dengue.png', dpi=300, bbox_inches='tight')
        plt.show()

def analisar_perfil_demografico(df):
    """
    Analisa o perfil demográfico dos casos
    """
    print("\nANALISE DEMOGRAFICA")
    print("=" * 50)
    
    # Análise por sexo
    if 'CS_SEXO' in df.columns:
        sexo_counts = df['CS_SEXO'].value_counts()
        print(f"Distribuicao por sexo:")
        print(f"   Feminino: {sexo_counts.get('F', 0)} casos")
        print(f"   Masculino: {sexo_counts.get('M', 0)} casos")
        
        # Gráfico de pizza
        plt.figure(figsize=(8, 6))
        sexo_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Distribuição dos Casos por Sexo')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig('distribuicao_sexo.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # Análise por idade
    if 'NU_IDADE_N' in df.columns:
        df['NU_IDADE_N'] = pd.to_numeric(df['NU_IDADE_N'], errors='coerce')
        
        # Criar faixas etárias
        df['FAIXA_ETARIA'] = pd.cut(df['NU_IDADE_N'], 
                                   bins=[0, 18, 30, 45, 60, 100], 
                                   labels=['0-17', '18-29', '30-44', '45-59', '60+'])
        
        faixas_counts = df['FAIXA_ETARIA'].value_counts()
        print(f"Distribuicao por faixa etaria:")
        for faixa, count in faixas_counts.items():
            print(f"   {faixa}: {count} casos")

def main():
    """
    Função principal que executa toda a análise
    """
    print("ANALISE DE DADOS DE DENGUE - CRICIÚMA/SC")
    print("=" * 60)
    print("Trabalho de Estatística Aplicada com Python e Pandas")
    print("=" * 60)
    
    # Carregar dados
    df = carregar_dados()
    if df is None:
        return
    
    # Explorar dados
    explorar_dados(df)
    
    # Identificar dados de Criciúma
    identificar_criciuma(df)
    
    # Análises adicionais
    analisar_casos_por_periodo(df)
    analisar_perfil_demografico(df)
    
    print("\nAnalise concluida!")
    print("Graficos salvos na pasta do projeto")
    print("Para analise completa, execute novamente com o dataset completo")

if __name__ == "__main__":
    main()
