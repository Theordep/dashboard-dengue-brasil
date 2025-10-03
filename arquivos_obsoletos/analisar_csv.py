#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar o arquivo DENGBR25.csv
"""

import pandas as pd

def analisar_csv():
    print("=== ANALISANDO O ARQUIVO DENGBR25.CSV ===")
    print("=" * 50)
    
    # Carregar dados
    df = pd.read_csv('Documentos/DENGBR25.csv', nrows=10000, low_memory=False)
    
    print(f"Total de registros analisados: {len(df):,}")
    print(f"Total de colunas: {len(df.columns)}")
    
    print("\n=== ANOS DISPONÍVEIS ===")
    anos = df['NU_ANO'].value_counts().sort_index()
    print(anos)
    
    print("\n=== ESTADOS COM MAIS CASOS ===")
    estados = df['SG_UF_NOT'].value_counts().head(10)
    for uf, casos in estados.items():
        print(f"UF {uf}: {casos:,} casos")
    
    print("\n=== SANTA CATARINA (UF 42) ===")
    sc = df[df['SG_UF_NOT'] == 42]
    print(f"Casos em SC: {len(sc)}")
    
    if len(sc) > 0:
        print("Municípios de SC com casos:")
        municipios_sc = sc['ID_MUNICIP'].value_counts()
        for codigo, casos in municipios_sc.head().items():
            print(f"  Código {codigo}: {casos} casos")
    
    print("\n=== CRICIÚMA ESPECÍFICO ===")
    criciuma = df[df['ID_MUNICIP'] == 4204608]
    print(f"Casos em Criciúma (4204608): {len(criciuma)}")
    
    print("\n=== SINTOMAS MAIS COMUNS ===")
    sintomas = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'EXANTEMA', 'VOMITO', 'NAUSEA']
    for sintoma in sintomas:
        if sintoma in df.columns:
            casos = (df[sintoma] == 1).sum()
            percentual = (casos / len(df)) * 100
            print(f"{sintoma}: {casos:,} casos ({percentual:.1f}%)")
    
    print("\n=== CLASSIFICAÇÃO DOS CASOS ===")
    if 'CLASSI_FIN' in df.columns:
        classif = df['CLASSI_FIN'].value_counts()
        print(classif)
    
    print("\n=== EVOLUÇÃO DOS CASOS ===")
    if 'EVOLUCAO' in df.columns:
        evol = df['EVOLUCAO'].value_counts()
        print(evol)
    
    print("\n=== DISTRIBUIÇÃO POR SEXO ===")
    if 'CS_SEXO' in df.columns:
        sexo = df['CS_SEXO'].value_counts()
        print(sexo)

if __name__ == "__main__":
    analisar_csv()
