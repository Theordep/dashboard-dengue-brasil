#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Apresentação para Workshop: Análise de Dengue com Python
Demonstração prática de Engenharia de Software + Estatística + Python

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

# Configuração para apresentação
plt.style.use('seaborn-v0_8')
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (14, 8)

def apresentacao_intro():
    """
    Introdução ao workshop
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
    Demonstração prática do carregamento de dados
    """
    print("\n1. CARREGAMENTO E EXPLORACAO DE DADOS")
    print("-" * 50)
    
    print("Carregando dados do DATASUS...")
    try:
        # Carregar uma amostra para demonstração
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
    Demonstração de análises estatísticas básicas
    """
    print("\n2️⃣ ANÁLISE ESTATÍSTICA")
    print("-" * 50)
    
    if df is None:
        return
    
    # Converter códigos para string
    df['SG_UF_NOT'] = df['SG_UF_NOT'].astype(str)
    
    # Análise por UF
    casos_por_uf = df['SG_UF_NOT'].value_counts().head(5)
    print("📊 Top 5 Estados com mais casos:")
    for uf, casos in casos_por_uf.items():
        percentual = (casos / len(df)) * 100
        print(f"   UF {uf}: {casos} casos ({percentual:.1f}%)")
    
    # Análise por sexo
    if 'CS_SEXO' in df.columns:
        sexo_dist = df['CS_SEXO'].value_counts()
        print(f"\n👥 Distribuição por sexo:")
        for sexo, casos in sexo_dist.items():
            percentual = (casos / len(df)) * 100
            print(f"   {sexo}: {casos} casos ({percentual:.1f}%)")
    
    # Análise de sintomas
    sintomas = ['FEBRE', 'MIALGIA', 'CEFALEIA']
    print(f"\n🦠 Sintomas mais comuns:")
    for sintoma in sintomas:
        if sintoma in df.columns:
            casos_com_sintoma = (df[sintoma] == 1).sum()
            percentual = (casos_com_sintoma / len(df)) * 100
            print(f"   {sintoma}: {casos_com_sintoma} casos ({percentual:.1f}%)")

def demonstrar_visualizacoes(df):
    """
    Demonstração de visualizações
    """
    print("\n3️⃣ CRIAÇÃO DE VISUALIZAÇÕES")
    print("-" * 50)
    
    if df is None:
        return
    
    # Configurar dados
    df['SG_UF_NOT'] = df['SG_UF_NOT'].astype(str)
    
    # Gráfico 1: Casos por UF
    plt.figure(figsize=(12, 6))
    casos_por_uf = df['SG_UF_NOT'].value_counts().head(8)
    casos_por_uf.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Casos de Dengue por UF - Workshop Demo', fontsize=16, fontweight='bold')
    plt.xlabel('UF', fontsize=12)
    plt.ylabel('Número de Casos', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('workshop_grafico_uf.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Gráfico 2: Distribuição por sexo
    if 'CS_SEXO' in df.columns:
        plt.figure(figsize=(8, 6))
        sexo_dist = df['CS_SEXO'].value_counts()
        cores = ['#ff9999', '#66b3ff', '#99ff99']
        sexo_dist.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=cores)
        plt.title('Distribuição por Sexo - Workshop Demo', fontsize=14, fontweight='bold')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig('workshop_grafico_sexo.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    print("✅ Gráficos salvos: workshop_grafico_uf.png, workshop_grafico_sexo.png")

def demonstrar_aplicacao_criciuma():
    """
    Demonstração da aplicação específica para Criciúma
    """
    print("\n4️⃣ APLICAÇÃO PARA CRICIÚMA")
    print("-" * 50)
    
    print("🏙️ Análise Específica de Criciúma/SC")
    print("\n📊 Situação Atual:")
    print("   • Código IBGE: 4204608")
    print("   • Casos em 2025: Não identificados na amostra")
    print("   • Necessário: Dados históricos e geográficos")
    
    print("\n🎯 Estratégias para Análise por Bairros:")
    print("   1. 📍 Coordenadas geográficas dos casos")
    print("   2. 🗺️ Mapa de bairros de Criciúma")
    print("   3. 📊 Dados do IBGE por setor censitário")
    print("   4. 🌡️ Correlação com dados climáticos")
    
    print("\n💡 Exemplo de Código para Análise por Bairro:")
    codigo_exemplo = '''
# Exemplo de análise por bairro
import geopandas as gpd
from shapely.geometry import Point

def analisar_por_bairro(casos_df, bairros_gdf):
    """
    Analisa casos de dengue por bairro
    """
    # 1. Criar pontos geográficos dos casos
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
    Demonstração de ferramentas avançadas
    """
    print("\n5️⃣ FERRAMENTAS AVANÇADAS")
    print("-" * 50)
    
    print("🚀 Próximas Evoluções:")
    
    ferramentas = {
        "🗺️ Mapas Interativos": "Folium + OpenStreetMap",
        "📊 Dashboards": "Streamlit ou Plotly Dash", 
        "🤖 Machine Learning": "Scikit-learn para predições",
        "📈 Séries Temporais": "Prophet ou ARIMA",
        "☁️ Deploy": "Heroku ou AWS",
        "📱 App Mobile": "Flutter + API Python"
    }
    
    for ferramenta, tecnologia in ferramentas.items():
        print(f"   {ferramenta}: {tecnologia}")
    
    print("\n💼 Aplicações Práticas:")
    aplicacoes = [
        "Sistema de alerta para autoridades de saúde",
        "Dashboard de monitoramento em tempo real", 
        "App para população reportar focos",
        "Análise preditiva de surtos",
        "Relatórios automatizados para gestores"
    ]
    
    for i, app in enumerate(aplicacoes, 1):
        print(f"   {i}. {app}")

def demonstrar_impacto_social():
    """
    Demonstração do impacto social
    """
    print("\n6️⃣ IMPACTO SOCIAL E COMUNITÁRIO")
    print("-" * 50)
    
    print("🌟 Como Engenharia de Software + Estatística podem ajudar:")
    
    impactos = {
        "🏥 Saúde Pública": "Identificação precoce de surtos",
        "💰 Gestão de Recursos": "Alocação eficiente de inseticidas",
        "👥 Educação": "Conscientização baseada em dados",
        "🏛️ Políticas Públicas": "Decisões baseadas em evidências",
        "🔬 Pesquisa": "Base para estudos epidemiológicos"
    }
    
    for area, beneficio in impactos.items():
        print(f"   {area}: {beneficio}")
    
    print("\n📊 Métricas de Sucesso:")
    metricas = [
        "Redução de 30% nos casos de dengue",
        "Detecção precoce de surtos em 48h",
        "Economia de R$ 500.000 em recursos",
        "Engajamento de 80% da população",
        "Base de dados para 5 pesquisas acadêmicas"
    ]
    
    for metrica in metricas:
        print(f"   • {metrica}")

def encerramento_workshop():
    """
    Encerramento do workshop
    """
    print("\n" + "=" * 80)
    print("🎉 ENCERRAMENTO DO WORKSHOP")
    print("=" * 80)
    
    print("\n📚 O que aprendemos hoje:")
    aprendizados = [
        "Como carregar e explorar grandes datasets",
        "Técnicas de análise estatística com Python",
        "Criação de visualizações profissionais",
        "Aplicação prática em dados de saúde",
        "Planejamento de análises geográficas"
    ]
    
    for i, aprendizado in enumerate(aprendizados, 1):
        print(f"   {i}. {aprendizado}")
    
    print("\n🚀 Próximos Passos:")
    print("   1. 📥 Baixar dados completos do DATASUS")
    print("   2. 🗺️ Obter dados geográficos de Criciúma")
    print("   3. 💻 Implementar análises por bairro")
    print("   4. 📊 Criar dashboard interativo")
    print("   5. 🎯 Apresentar resultados para a comunidade")
    
    print("\n💡 Recursos Adicionais:")
    recursos = [
        "Documentação do Pandas: pandas.pydata.org",
        "Tutoriais de Matplotlib: matplotlib.org/tutorials",
        "Dados do IBGE: ibge.gov.br",
        "DATASUS: datasus.gov.br",
        "Comunidade Python Brasil: python.org.br"
    ]
    
    for recurso in recursos:
        print(f"   • {recurso}")
    
    print("\n" + "=" * 80)
    print("🤝 OBRIGADO PELA PARTICIPAÇÃO!")
    print("💬 Dúvidas? Entre em contato!")
    print("=" * 80)

def main():
    """
    Função principal do workshop
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
