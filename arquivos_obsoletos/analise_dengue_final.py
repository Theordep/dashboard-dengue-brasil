#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise de Dados de Dengue - Análise Geral e Preparação para Criciúma
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

def carregar_e_explorar_dados():
    """
    Carrega e explora os dados do arquivo CSV do DATASUS
    """
    print("Carregando dados do DENGBR25.csv...")
    
    try:
        # Carregar uma amostra significativa
        df = pd.read_csv('Documentos/DENGBR25.csv', nrows=50000, low_memory=False)
        print(f"Dados carregados com sucesso! Shape: {df.shape}")
        
        # Converter códigos para string para evitar problemas
        if 'ID_MUNICIP' in df.columns:
            df['ID_MUNICIP'] = df['ID_MUNICIP'].astype(str)
        if 'SG_UF_NOT' in df.columns:
            df['SG_UF_NOT'] = df['SG_UF_NOT'].astype(str)
        
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None

def analisar_distribuicao_geografica(df):
    """
    Analisa a distribuição geográfica dos casos
    """
    print("\nANALISE GEOGRAFICA DOS CASOS")
    print("=" * 50)
    
    if 'SG_UF_NOT' in df.columns:
        # Contar casos por UF
        casos_por_uf = df['SG_UF_NOT'].value_counts().head(10)
        print("Top 10 estados com mais casos:")
        for uf, casos in casos_por_uf.items():
            print(f"  UF {uf}: {casos} casos")
        
        # Verificar se há casos em Santa Catarina (42)
        sc_casos = df[df['SG_UF_NOT'] == '42']
        print(f"\nCasos em Santa Catarina (UF 42): {len(sc_casos)}")
        
        if len(sc_casos) > 0:
            print("Municípios de SC com casos:")
            if 'ID_MUNICIP' in sc_casos.columns:
                municipios_sc = sc_casos['ID_MUNICIP'].value_counts()
                for codigo, casos in municipios_sc.head(10).items():
                    print(f"  {codigo}: {casos} casos")
        
        # Plotar distribuição por UF
        plt.figure(figsize=(14, 8))
        casos_por_uf.plot(kind='bar')
        plt.title('Distribuicao de Casos de Dengue por UF')
        plt.xlabel('UF')
        plt.ylabel('Numero de Casos')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('distribuicao_por_uf.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    return sc_casos if 'SG_UF_NOT' in df.columns else pd.DataFrame()

def analisar_perfil_demografico(df):
    """
    Analisa o perfil demográfico dos casos
    """
    print("\nANALISE DEMOGRAFICA")
    print("=" * 50)
    
    # Análise por sexo
    if 'CS_SEXO' in df.columns:
        sexo_counts = df['CS_SEXO'].value_counts()
        print("Distribuicao por sexo:")
        print(f"  Feminino: {sexo_counts.get('F', 0)} casos")
        print(f"  Masculino: {sexo_counts.get('M', 0)} casos")
        print(f"  Ignorado: {sexo_counts.get('I', 0)} casos")
        
        # Gráfico de pizza
        plt.figure(figsize=(10, 6))
        sexo_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Distribuicao dos Casos por Sexo')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig('distribuicao_sexo.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # Análise por idade
    if 'NU_IDADE_N' in df.columns:
        df['IDADE_NUM'] = pd.to_numeric(df['NU_IDADE_N'], errors='coerce')
        idades_validas = df['IDADE_NUM'].notna()
        
        if idades_validas.sum() > 0:
            print(f"\nEstatisticas de idade:")
            print(f"  Idade media: {df['IDADE_NUM'].mean():.1f} anos")
            print(f"  Idade mediana: {df['IDADE_NUM'].median():.1f} anos")
            print(f"  Faixa de idade: {df['IDADE_NUM'].min():.0f} - {df['IDADE_NUM'].max():.0f} anos")
            
            # Criar faixas etárias
            df['FAIXA_ETARIA'] = pd.cut(df['IDADE_NUM'], 
                                       bins=[0, 18, 30, 45, 60, 100], 
                                       labels=['0-17', '18-29', '30-44', '45-59', '60+'])
            
            faixas_counts = df['FAIXA_ETARIA'].value_counts()
            print(f"\nDistribuicao por faixa etaria:")
            for faixa, count in faixas_counts.items():
                percentual = (count / len(df)) * 100
                print(f"  {faixa}: {count} casos ({percentual:.1f}%)")
            
            # Histograma de idades
            plt.figure(figsize=(10, 6))
            df['IDADE_NUM'].hist(bins=20, edgecolor='black')
            plt.title('Distribuicao de Idades dos Casos de Dengue')
            plt.xlabel('Idade (anos)')
            plt.ylabel('Frequencia')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('distribuicao_idades.png', dpi=300, bbox_inches='tight')
            plt.show()

def analisar_temporal(df):
    """
    Analisa a evolução temporal dos casos
    """
    print("\nANALISE TEMPORAL")
    print("=" * 50)
    
    if 'DT_NOTIFIC' in df.columns:
        df['DT_NOTIFIC_CLEAN'] = pd.to_datetime(df['DT_NOTIFIC'], errors='coerce')
        datas_validas = df['DT_NOTIFIC_CLEAN'].notna().sum()
        
        print(f"Datas validas: {datas_validas} de {len(df)} registros")
        
        if datas_validas > 0:
            df['MES'] = df['DT_NOTIFIC_CLEAN'].dt.month
            df['ANO'] = df['DT_NOTIFIC_CLEAN'].dt.year
            
            # Casos por mês
            casos_mes = df.groupby('MES').size()
            print(f"\nCasos por mes:")
            meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                          'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            for mes, casos in casos_mes.items():
                if not pd.isna(mes):
                    print(f"  {meses_nomes[int(mes)-1]}: {casos} casos")
            
            # Gráfico temporal
            plt.figure(figsize=(12, 6))
            casos_mes.plot(kind='bar')
            plt.title('Distribuicao de Casos por Mes')
            plt.xlabel('Mes')
            plt.ylabel('Numero de Casos')
            plt.xticks(range(len(meses_nomes)), meses_nomes, rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('casos_por_mes.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    # Análise por ano
    if 'NU_ANO' in df.columns:
        casos_ano = df['NU_ANO'].value_counts().sort_index()
        print(f"\nCasos por ano:")
        for ano, casos in casos_ano.items():
            print(f"  {ano}: {casos} casos")

def analisar_sintomas(df):
    """
    Analisa os sintomas mais comuns
    """
    print("\nANALISE DE SINTOMAS")
    print("=" * 50)
    
    sintomas = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'EXANTEMA', 'VOMITO', 
                'NAUSEA', 'DOR_COSTAS', 'CONJUNTVIT', 'ARTRITE', 'ARTRALGIA']
    
    sintomas_contagem = {}
    
    for sintoma in sintomas:
        if sintoma in df.columns:
            casos_com_sintoma = (df[sintoma] == 1).sum()
            sintomas_contagem[sintoma] = casos_com_sintoma
    
    if sintomas_contagem:
        print("Sintomas mais comuns (valor 1 = presente):")
        for sintoma, count in sorted(sintomas_contagem.items(), key=lambda x: x[1], reverse=True):
            percentual = (count / len(df)) * 100
            print(f"  {sintoma}: {count} casos ({percentual:.1f}%)")
        
        # Gráfico de sintomas
        plt.figure(figsize=(12, 8))
        sintomas_df = pd.DataFrame(list(sintomas_contagem.items()), 
                                  columns=['Sintoma', 'Casos'])
        sintomas_df = sintomas_df.sort_values('Casos', ascending=True)
        
        plt.barh(sintomas_df['Sintoma'], sintomas_df['Casos'])
        plt.title('Sintomas Mais Comuns nos Casos de Dengue')
        plt.xlabel('Numero de Casos')
        plt.tight_layout()
        plt.savefig('sintomas_comuns.png', dpi=300, bbox_inches='tight')
        plt.show()

def analisar_classificacao_evolucao(df):
    """
    Analisa classificação final e evolução dos casos
    """
    print("\nANALISE DE CLASSIFICACAO E EVOLUCAO")
    print("=" * 50)
    
    # Classificação final
    if 'CLASSI_FIN' in df.columns:
        classif_counts = df['CLASSI_FIN'].value_counts()
        print("Classificacao final dos casos:")
        for classif, count in classif_counts.items():
            percentual = (count / len(df)) * 100
            print(f"  {classif}: {count} casos ({percentual:.1f}%)")
    
    # Evolução dos casos
    if 'EVOLUCAO' in df.columns:
        evolucao_counts = df['EVOLUCAO'].value_counts()
        print(f"\nEvolucao dos casos:")
        evolucao_nomes = {
            1: 'Cura',
            2: 'Obito por dengue',
            3: 'Obito por outras causas',
            4: 'Obito em investigacao',
            9: 'Ignorado'
        }
        
        for evolucao, count in evolucao_counts.items():
            if not pd.isna(evolucao):
                nome = evolucao_nomes.get(int(evolucao), f'Codigo {evolucao}')
                percentual = (count / len(df)) * 100
                print(f"  {nome}: {count} casos ({percentual:.1f}%)")

def preparar_analise_criciuma():
    """
    Prepara sugestões para análise específica de Criciúma
    """
    print("\nPREPARACAO PARA ANALISE DE CRICIÚMA")
    print("=" * 50)
    
    print("Para uma analise completa de Criciúma, sugere-se:")
    print("\n1. OBTER DADOS COMPLETOS:")
    print("   - Baixar dataset completo do DATASUS (sem limite de linhas)")
    print("   - Verificar se há dados históricos de anos anteriores")
    print("   - Obter dados de 2024 e anos anteriores para comparacao")
    
    print("\n2. IDENTIFICAR CRICIÚMA:")
    print("   - Codigo IBGE: 4204608")
    print("   - Verificar se o dataset usa códigos diferentes")
    print("   - Buscar por variacoes do nome (CRICIÚMA, CRICIÚMA/SC)")
    
    print("\n3. DADOS GEOGRAFICOS DETALHADOS:")
    print("   - Obter mapa de bairros de Criciúma")
    print("   - Correlacionar com códigos de CEP ou setores censitários")
    print("   - Usar dados do IBGE para delimitação de bairros")
    
    print("\n4. ANALISES SUGERIDAS:")
    print("   - Casos por bairro (usando coordenadas geográficas)")
    print("   - Densidade de casos por área")
    print("   - Correlação com fatores socioeconômicos")
    print("   - Análise sazonal específica da região")
    print("   - Comparação com outras cidades de SC")
    
    print("\n5. FONTES DE DADOS ADICIONAIS:")
    print("   - Prefeitura de Criciúma (Secretaria de Saúde)")
    print("   - IBGE (dados demográficos por bairro)")
    print("   - INMET (dados climáticos)")
    print("   - DATASUS (dados históricos completos)")

def criar_script_criciuma():
    """
    Cria um script específico para análise de Criciúma
    """
    script_content = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Análise Específica de Dengue em Criciúma/SC
Para usar quando dados completos estiverem disponíveis
"""

import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point

def analisar_criciuma_completo():
    """
    Função para análise completa quando dados estiverem disponíveis
    """
    # 1. Carregar dados completos
    df = pd.read_csv('DENGBR25.csv', low_memory=False)
    
    # 2. Filtrar Criciúma
    criciuma = df[df['ID_MUNICIP'] == '4204608']
    
    # 3. Análises por bairro (requer dados geográficos)
    # - Usar coordenadas se disponíveis
    # - Correlacionar com setores censitários do IBGE
    
    # 4. Visualizações específicas
    # - Mapa de calor por bairro
    # - Análise temporal específica
    # - Correlação com dados climáticos
    
    pass

# Execute quando dados completos estiverem disponíveis
if __name__ == "__main__":
    analisar_criciuma_completo()
'''
    
    with open('script_criciuma_especifico.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("Script específico para Criciúma criado: script_criciuma_especifico.py")

def main():
    """
    Função principal da análise
    """
    print("ANALISE DE DADOS DE DENGUE - PREPARACAO PARA CRICIÚMA")
    print("=" * 70)
    print("Trabalho de Estatística Aplicada com Python e Pandas")
    print("=" * 70)
    
    # Carregar dados
    df = carregar_e_explorar_dados()
    if df is None:
        return
    
    # Análises gerais
    sc_casos = analisar_distribuicao_geografica(df)
    analisar_perfil_demografico(df)
    analisar_temporal(df)
    analisar_sintomas(df)
    analisar_classificacao_evolucao(df)
    
    # Preparação para Criciúma
    preparar_analise_criciuma()
    criar_script_criciuma()
    
    print("\n" + "="*70)
    print("ANALISE CONCLUIDA!")
    print("="*70)
    print("Próximos passos:")
    print("1. Verificar se há dados históricos de anos anteriores")
    print("2. Obter dados completos do DATASUS")
    print("3. Buscar dados geográficos específicos de Criciúma")
    print("4. Executar script específico quando dados estiverem disponíveis")
    print("\nGráficos salvos na pasta do projeto!")

if __name__ == "__main__":
    main()
