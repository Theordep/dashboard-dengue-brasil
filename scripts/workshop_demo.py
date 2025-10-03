#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo do Workshop: Analise de Dengue com Python
Demonstracao pratica de Engenharia de Software + Estatistica + Python
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Configuracao para apresentacao
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (14, 8)

def apresentacao_intro():
    """
    Introducao ao workshop
    """
    print("=" * 80)
    print("WORKSHOP: ANALISE DE DENGUE COM PYTHON E PANDAS")
    print("=" * 80)
    print("Engenharia de Software + Estatistica + Python")
    print("Objetivo: Demonstrar aplicacao pratica em dados reais de saude")
    print("Foco: Criciuma/SC e analise por bairros")
    print("=" * 80)
    
    print("\nAGENDA DO WORKSHOP:")
    print("1. Apresentacao do problema")
    print("2. Exploracao dos dados")
    print("3. Analise estatistica")
    print("4. Visualizacoes")
    print("5. Aplicacao para Criciuma")
    print("6. Proximos passos")
    print("=" * 80)

def demonstrar_carregamento_dados():
    """
    Demonstracao pratica do carregamento de dados
    """
    print("\n1. CARREGAMENTO E EXPLORACAO DE DADOS")
    print("-" * 50)
    
    print("Carregando dados do DATASUS...")
    try:
        # Carregar uma amostra para demonstracao
        df = pd.read_csv('Documentos/DENGBR25.csv', nrows=5000, low_memory=False)
        print(f"Dados carregados: {df.shape[0]} linhas x {df.shape[1]} colunas")
        
        print(f"\nColunas principais:")
        colunas_principais = ['SG_UF_NOT', 'ID_MUNICIP', 'DT_NOTIFIC', 'CS_SEXO', 
                             'NU_IDADE_N', 'FEBRE', 'MIALGIA', 'CEFALEIA']
        for col in colunas_principais:
            if col in df.columns:
                print(f"   - {col}")
        
        print(f"\nPrimeiras 3 linhas:")
        print(df[colunas_principais].head(3))
        
        return df
        
    except Exception as e:
        print(f"Erro: {e}")
        return None

def demonstrar_analise_estatistica(df):
    """
    Demonstracao de analises estatisticas basicas
    """
    print("\n2. ANALISE ESTATISTICA")
    print("-" * 50)
    
    if df is None:
        return
    
    # Converter codigos para string
    df['SG_UF_NOT'] = df['SG_UF_NOT'].astype(str)
    
    # Analise por UF
    casos_por_uf = df['SG_UF_NOT'].value_counts().head(5)
    print("Top 5 Estados com mais casos:")
    for uf, casos in casos_por_uf.items():
        percentual = (casos / len(df)) * 100
        print(f"   UF {uf}: {casos} casos ({percentual:.1f}%)")
    
    # Analise por sexo
    if 'CS_SEXO' in df.columns:
        sexo_dist = df['CS_SEXO'].value_counts()
        print(f"\nDistribuicao por sexo:")
        for sexo, casos in sexo_dist.items():
            percentual = (casos / len(df)) * 100
            print(f"   {sexo}: {casos} casos ({percentual:.1f}%)")
    
    # Analise de sintomas
    sintomas = ['FEBRE', 'MIALGIA', 'CEFALEIA']
    print(f"\nSintomas mais comuns:")
    for sintoma in sintomas:
        if sintoma in df.columns:
            casos_com_sintoma = (df[sintoma] == 1).sum()
            percentual = (casos_com_sintoma / len(df)) * 100
            print(f"   {sintoma}: {casos_com_sintoma} casos ({percentual:.1f}%)")

def demonstrar_visualizacoes(df):
    """
    Demonstracao de visualizacoes
    """
    print("\n3. CRIACAO DE VISUALIZACOES")
    print("-" * 50)
    
    if df is None:
        return
    
    # Configurar dados
    df['SG_UF_NOT'] = df['SG_UF_NOT'].astype(str)
    
    # Grafico 1: Casos por UF
    plt.figure(figsize=(12, 6))
    casos_por_uf = df['SG_UF_NOT'].value_counts().head(8)
    casos_por_uf.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Casos de Dengue por UF - Workshop Demo', fontsize=16, fontweight='bold')
    plt.xlabel('UF', fontsize=12)
    plt.ylabel('Numero de Casos', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('workshop_grafico_uf.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Grafico 2: Distribuicao por sexo
    if 'CS_SEXO' in df.columns:
        plt.figure(figsize=(8, 6))
        sexo_dist = df['CS_SEXO'].value_counts()
        cores = ['#ff9999', '#66b3ff', '#99ff99']
        sexo_dist.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=cores)
        plt.title('Distribuicao por Sexo - Workshop Demo', fontsize=14, fontweight='bold')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig('workshop_grafico_sexo.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    print("Graficos salvos: workshop_grafico_uf.png, workshop_grafico_sexo.png")

def demonstrar_aplicacao_criciuma():
    """
    Demonstracao da aplicacao especifica para Criciuma
    """
    print("\n4. APLICACAO PARA CRICIÚMA")
    print("-" * 50)
    
    print("Analise Especifica de Criciuma/SC")
    print("\nSituacao Atual:")
    print("   - Codigo IBGE: 4204608")
    print("   - Casos em 2025: Nao identificados na amostra")
    print("   - Necessario: Dados historicos e geograficos")
    
    print("\nEstrategias para Analise por Bairros:")
    print("   1. Coordenadas geograficas dos casos")
    print("   2. Mapa de bairros de Criciuma")
    print("   3. Dados do IBGE por setor censitario")
    print("   4. Correlacao com dados climaticos")
    
    print("\nExemplo de Codigo para Analise por Bairro:")
    codigo_exemplo = '''
# Exemplo de analise por bairro
import geopandas as gpd
from shapely.geometry import Point

def analisar_por_bairro(casos_df, bairros_gdf):
    """
    Analisa casos de dengue por bairro
    """
    # 1. Criar pontos geograficos dos casos
    geometria_casos = [Point(xy) for xy in zip(casos_df['LONGITUDE'], 
                                              casos_df['LATITUDE'])]
    casos_gdf = gpd.GeoDataFrame(casos_df, geometry=geometria_casos)
    
    # 2. Fazer join espacial com bairros
    casos_por_bairro = gpd.sjoin(casos_gdf, bairros_gdf, how='left')
    
    # 3. Contar casos por bairro
    contagem_bairros = casos_por_bairro.groupby('NOME_BAIRRO').size()
    
    return contagem_bairros
'''
    print(codigo_exemplo)

def demonstrar_ferramentas_avancadas():
    """
    Demonstracao de ferramentas avancadas
    """
    print("\n5. FERRAMENTAS AVANCADAS")
    print("-" * 50)
    
    print("Proximas Evolucoes:")
    
    ferramentas = {
        "Mapas Interativos": "Folium + OpenStreetMap",
        "Dashboards": "Streamlit ou Plotly Dash", 
        "Machine Learning": "Scikit-learn para predicoes",
        "Series Temporais": "Prophet ou ARIMA",
        "Deploy": "Heroku ou AWS",
        "App Mobile": "Flutter + API Python"
    }
    
    for ferramenta, tecnologia in ferramentas.items():
        print(f"   {ferramenta}: {tecnologia}")
    
    print("\nAplicacoes Praticas:")
    aplicacoes = [
        "Sistema de alerta para autoridades de saude",
        "Dashboard de monitoramento em tempo real", 
        "App para populacao reportar focos",
        "Analise preditiva de surtos",
        "Relatorios automatizados para gestores"
    ]
    
    for i, app in enumerate(aplicacoes, 1):
        print(f"   {i}. {app}")

def demonstrar_impacto_social():
    """
    Demonstracao do impacto social
    """
    print("\n6. IMPACTO SOCIAL E COMUNITARIO")
    print("-" * 50)
    
    print("Como Engenharia de Software + Estatistica podem ajudar:")
    
    impactos = {
        "Saude Publica": "Identificacao precoce de surtos",
        "Gestao de Recursos": "Alocacao eficiente de inseticidas",
        "Educacao": "Conscientizacao baseada em dados",
        "Politicas Publicas": "Decisoes baseadas em evidencias",
        "Pesquisa": "Base para estudos epidemiologicos"
    }
    
    for area, beneficio in impactos.items():
        print(f"   {area}: {beneficio}")
    
    print("\nMetricas de Sucesso:")
    metricas = [
        "Reducao de 30% nos casos de dengue",
        "Deteccao precoce de surtos em 48h",
        "Economia de R$ 500.000 em recursos",
        "Engajamento de 80% da populacao",
        "Base de dados para 5 pesquisas academicas"
    ]
    
    for metrica in metricas:
        print(f"   - {metrica}")

def encerramento_workshop():
    """
    Encerramento do workshop
    """
    print("\n" + "=" * 80)
    print("ENCERRAMENTO DO WORKSHOP")
    print("=" * 80)
    
    print("\nO que aprendemos hoje:")
    aprendizados = [
        "Como carregar e explorar grandes datasets",
        "Tecnicas de analise estatistica com Python",
        "Criacao de visualizacoes profissionais",
        "Aplicacao pratica em dados de saude",
        "Planejamento de analises geograficas"
    ]
    
    for i, aprendizado in enumerate(aprendizados, 1):
        print(f"   {i}. {aprendizado}")
    
    print("\nProximos Passos:")
    print("   1. Baixar dados completos do DATASUS")
    print("   2. Obter dados geograficos de Criciuma")
    print("   3. Implementar analises por bairro")
    print("   4. Criar dashboard interativo")
    print("   5. Apresentar resultados para a comunidade")
    
    print("\nRecursos Adicionais:")
    recursos = [
        "Documentacao do Pandas: pandas.pydata.org",
        "Tutoriais de Matplotlib: matplotlib.org/tutorials",
        "Dados do IBGE: ibge.gov.br",
        "DATASUS: datasus.gov.br",
        "Comunidade Python Brasil: python.org.br"
    ]
    
    for recurso in recursos:
        print(f"   - {recurso}")
    
    print("\n" + "=" * 80)
    print("OBRIGADO PELA PARTICIPACAO!")
    print("Duvidas? Entre em contato!")
    print("=" * 80)

def main():
    """
    Funcao principal do workshop
    """
    # Executar todas as etapas do workshop
    apresentacao_intro()
    
    df = demonstrar_carregamento_dados()
    
    demonstrar_analise_estatistica(df)
    demonstrar_visualizacoes(df)
    demonstrar_aplicacao_criciuma()
    demonstrar_ferramentas_avancadas()
    demonstrar_impacto_social()
    encerramento_workshop()

if __name__ == "__main__":
    main()
