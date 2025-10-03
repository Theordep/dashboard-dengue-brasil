#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise de Dados de Dengue - Criciúma/SC (Versão Melhorada)
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

def carregar_dados_completo():
    """
    Carrega os dados do arquivo CSV do DATASUS de forma mais robusta
    """
    print("Carregando dados do DENGBR25.csv...")
    
    try:
        # Primeiro, vamos carregar apenas o cabeçalho para entender a estrutura
        df_header = pd.read_csv('Documentos/DENGBR25.csv', nrows=0)
        print(f"Dataset possui {len(df_header.columns)} colunas")
        
        # Agora carregar uma amostra maior para análise
        df = pd.read_csv('Documentos/DENGBR25.csv', nrows=10000, low_memory=False)
        print(f"Dados carregados com sucesso! Shape: {df.shape}")
        
        # Verificar se há dados de 2025 (que parece ser o ano dos dados)
        if 'NU_ANO' in df.columns:
            anos_unicos = df['NU_ANO'].unique()
            print(f"Anos encontrados: {sorted(anos_unicos)}")
        
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None

def explorar_estrutura_dados(df):
    """
    Explora a estrutura dos dados de forma mais detalhada
    """
    print("\nEXPLORACAO DETALHADA DOS DADOS")
    print("=" * 50)
    
    print(f"Dimensoes: {df.shape[0]} linhas x {df.shape[1]} colunas")
    
    # Analisar colunas importantes
    colunas_importantes = {
        'SG_UF_NOT': 'UF de notificação',
        'ID_MUNICIP': 'Código do município',
        'MUNICIPIO': 'Nome do município',
        'DT_NOTIFIC': 'Data de notificação',
        'NU_ANO': 'Ano',
        'CS_SEXO': 'Sexo',
        'NU_IDADE_N': 'Idade',
        'CLASSI_FIN': 'Classificação final',
        'EVOLUCAO': 'Evolução do caso'
    }
    
    print("\nColunas importantes encontradas:")
    for col, desc in colunas_importantes.items():
        if col in df.columns:
            print(f"  {col}: {desc}")
            print(f"    Tipo: {df[col].dtype}")
            print(f"    Valores únicos: {df[col].nunique()}")
            if df[col].nunique() <= 10:
                print(f"    Valores: {df[col].unique()}")
            print()
    
    # Verificar dados de Santa Catarina
    if 'SG_UF_NOT' in df.columns:
        sc_data = df[df['SG_UF_NOT'] == '42']  # SC = 42
        print(f"Casos em Santa Catarina: {len(sc_data)}")
        
        if 'ID_MUNICIP' in sc_data.columns:
            municipios_sc = sc_data['ID_MUNICIP'].value_counts().head(10)
            print("Top 10 municípios de SC por código:")
            for codigo, casos in municipios_sc.items():
                print(f"  {codigo}: {casos} casos")

def identificar_criciuma_corrigido(df):
    """
    Identifica dados de Criciúma usando diferentes abordagens
    """
    print("\nIDENTIFICANDO DADOS DE CRICIÚMA")
    print("=" * 50)
    
    # Criciúma tem código IBGE 4204608
    # Mas vamos verificar se os dados usam códigos diferentes
    
    if 'SG_UF_NOT' in df.columns and 'ID_MUNICIP' in df.columns:
        # Filtrar apenas Santa Catarina
        sc_data = df[df['SG_UF_NOT'] == '42']
        print(f"Total de casos em Santa Catarina: {len(sc_data)}")
        
        # Verificar códigos de municípios em SC
        codigos_sc = sc_data['ID_MUNICIP'].value_counts()
        print(f"\nCódigos de municípios encontrados em SC:")
        for codigo, casos in codigos_sc.head(15).items():
            print(f"  {codigo}: {casos} casos")
        
        # Procurar por Criciúma usando código 4204608
        criciuma_por_codigo = sc_data[sc_data['ID_MUNICIP'] == '4204608']
        print(f"\nCasos com código 4204608 (Criciúma): {len(criciuma_por_codigo)}")
        
        # Se não encontrar, vamos verificar se há outros códigos
        if len(criciuma_por_codigo) == 0:
            print("Código 4204608 não encontrado. Verificando outros códigos...")
            
            # Verificar se há códigos que começam com 4204 (região de Criciúma)
            codigos_4204 = sc_data[sc_data['ID_MUNICIP'].str.startswith('4204', na=False)]
            if len(codigos_4204) > 0:
                print(f"Códigos que começam com 4204: {codigos_4204['ID_MUNICIP'].unique()}")
        
        return criciuma_por_codigo, sc_data
    
    return None, None

def analisar_casos_por_periodo_corrigido(df):
    """
    Analisa casos por período temporal com tratamento de dados
    """
    print("\nANALISE TEMPORAL DOS CASOS")
    print("=" * 50)
    
    if 'DT_NOTIFIC' in df.columns:
        # Converter data, tratando erros
        df['DT_NOTIFIC_CLEAN'] = pd.to_datetime(df['DT_NOTIFIC'], errors='coerce')
        
        # Verificar quantas datas válidas temos
        datas_validas = df['DT_NOTIFIC_CLEAN'].notna().sum()
        print(f"Datas válidas: {datas_validas} de {len(df)} registros")
        
        if datas_validas > 0:
            # Extrair mês e ano
            df['MES'] = df['DT_NOTIFIC_CLEAN'].dt.month
            df['ANO'] = df['DT_NOTIFIC_CLEAN'].dt.year
            
            # Casos por mês/ano
            casos_temporais = df.groupby(['ANO', 'MES']).size().reset_index(name='CASOS')
            print(f"\nCasos por período:")
            print(casos_temporais.head(10))
            
            # Plotar evolução temporal
            plt.figure(figsize=(12, 6))
            casos_temporais_plot = casos_temporais.set_index(['ANO', 'MES'])
            casos_temporais_plot.plot(kind='line', marker='o')
            plt.title('Evolucao dos Casos de Dengue por Mes/Ano')
            plt.xlabel('Período')
            plt.ylabel('Numero de Casos')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('evolucao_casos_dengue.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    # Análise por ano se disponível
    if 'NU_ANO' in df.columns:
        casos_ano = df['NU_ANO'].value_counts().sort_index()
        print(f"\nCasos por ano:")
        for ano, casos in casos_ano.items():
            print(f"  {ano}: {casos} casos")

def analisar_perfil_demografico_corrigido(df):
    """
    Analisa o perfil demográfico dos casos com tratamento de dados
    """
    print("\nANALISE DEMOGRAFICA")
    print("=" * 50)
    
    # Análise por sexo
    if 'CS_SEXO' in df.columns:
        sexo_counts = df['CS_SEXO'].value_counts()
        print(f"Distribuicao por sexo:")
        print(f"  Feminino: {sexo_counts.get('F', 0)} casos")
        print(f"  Masculino: {sexo_counts.get('M', 0)} casos")
        
        # Gráfico de pizza
        plt.figure(figsize=(8, 6))
        sexo_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Distribuicao dos Casos por Sexo')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig('distribuicao_sexo.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # Análise por idade
    if 'NU_IDADE_N' in df.columns:
        # Converter idade para numérico
        df['IDADE_NUM'] = pd.to_numeric(df['NU_IDADE_N'], errors='coerce')
        
        # Estatísticas básicas de idade
        idades_validas = df['IDADE_NUM'].notna()
        print(f"Idades válidas: {idades_validas.sum()} de {len(df)} registros")
        
        if idades_validas.sum() > 0:
            print(f"Idade média: {df['IDADE_NUM'].mean():.1f} anos")
            print(f"Idade mediana: {df['IDADE_NUM'].median():.1f} anos")
            print(f"Faixa de idade: {df['IDADE_NUM'].min():.0f} - {df['IDADE_NUM'].max():.0f} anos")
            
            # Criar faixas etárias
            df['FAIXA_ETARIA'] = pd.cut(df['IDADE_NUM'], 
                                       bins=[0, 18, 30, 45, 60, 100], 
                                       labels=['0-17', '18-29', '30-44', '45-59', '60+'])
            
            faixas_counts = df['FAIXA_ETARIA'].value_counts()
            print(f"\nDistribuicao por faixa etaria:")
            for faixa, count in faixas_counts.items():
                print(f"  {faixa}: {count} casos")
    
    # Análise por classificação final
    if 'CLASSI_FIN' in df.columns:
        classif_counts = df['CLASSI_FIN'].value_counts()
        print(f"\nClassificacao final dos casos:")
        for classif, count in classif_counts.items():
            print(f"  {classif}: {count} casos")

def analisar_sintomas(df):
    """
    Analisa os sintomas mais comuns nos casos de dengue
    """
    print("\nANALISE DE SINTOMAS")
    print("=" * 50)
    
    # Sintomas disponíveis no dataset
    sintomas = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'EXANTEMA', 'VOMITO', 
                'NAUSEA', 'DOR_COSTAS', 'CONJUNTVIT', 'ARTRITE', 'ARTRALGIA']
    
    sintomas_contagem = {}
    
    for sintoma in sintomas:
        if sintoma in df.columns:
            # Contar casos onde o sintoma está presente (valor 1)
            casos_com_sintoma = (df[sintoma] == 1).sum()
            sintomas_contagem[sintoma] = casos_com_sintoma
    
    if sintomas_contagem:
        print("Sintomas mais comuns:")
        for sintoma, count in sorted(sintomas_contagem.items(), key=lambda x: x[1], reverse=True):
            percentual = (count / len(df)) * 100
            print(f"  {sintoma}: {count} casos ({percentual:.1f}%)")

def criar_relatorio_final(df, criciuma_data=None):
    """
    Cria um relatório final da análise
    """
    print("\nRELATORIO FINAL DA ANALISE")
    print("=" * 50)
    
    print(f"Total de registros analisados: {len(df)}")
    
    if 'SG_UF_NOT' in df.columns:
        ufs = df['SG_UF_NOT'].value_counts()
        print(f"Estados com mais casos:")
        for uf, casos in ufs.head(5).items():
            print(f"  UF {uf}: {casos} casos")
    
    if criciuma_data is not None and len(criciuma_data) > 0:
        print(f"\nCasos específicos de Criciúma: {len(criciuma_data)}")
        
        if 'CS_SEXO' in criciuma_data.columns:
            sexo_criciuma = criciuma_data['CS_SEXO'].value_counts()
            print(f"Distribuição por sexo em Criciúma:")
            for sexo, casos in sexo_criciuma.items():
                print(f"  {sexo}: {casos} casos")
    
    print(f"\nPróximos passos sugeridos:")
    print("1. Carregar dataset completo para análise mais abrangente")
    print("2. Obter dados geográficos detalhados (bairros de Criciúma)")
    print("3. Correlacionar com dados climáticos")
    print("4. Analisar tendências sazonais")
    print("5. Identificar fatores de risco por região")

def main():
    """
    Função principal que executa toda a análise melhorada
    """
    print("ANALISE DE DADOS DE DENGUE - CRICIÚMA/SC (VERSÃO MELHORADA)")
    print("=" * 70)
    print("Trabalho de Estatística Aplicada com Python e Pandas")
    print("=" * 70)
    
    # Carregar dados
    df = carregar_dados_completo()
    if df is None:
        return
    
    # Explorar estrutura
    explorar_estrutura_dados(df)
    
    # Identificar dados de Criciúma
    criciuma_data, sc_data = identificar_criciuma_corrigido(df)
    
    # Análises detalhadas
    analisar_casos_por_periodo_corrigido(df)
    analisar_perfil_demografico_corrigido(df)
    analisar_sintomas(df)
    
    # Relatório final
    criar_relatorio_final(df, criciuma_data)
    
    print("\nAnalise concluida!")
    print("Graficos salvos na pasta do projeto")
    print("Para analise completa com todos os dados, modifique o parametro nrows no carregamento")

if __name__ == "__main__":
    main()
