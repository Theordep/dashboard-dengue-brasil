#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar os dados de idade no CSV
"""

import pandas as pd
import numpy as np

def main():
    print("Verificando dados de idade no CSV...")
    
    try:
        # Carregar o CSV
        csv_path = 'Documentos/DENGBR25.csv'
        df = pd.read_csv(csv_path, low_memory=False)
        
        # Verificar total de registros
        total_registros = len(df)
        print(f"Total de registros: {total_registros:,}")
        
        # Verificar se a coluna de idade existe
        if 'NU_IDADE_N' not in df.columns:
            print("ERRO: Coluna NU_IDADE_N não encontrada!")
            print("Colunas disponíveis:", df.columns.tolist())
            return
            
        # Converter para numérico
        df['NU_IDADE_N'] = pd.to_numeric(df['NU_IDADE_N'], errors='coerce')
        
        # Verificar valores nulos
        nulos = df['NU_IDADE_N'].isna().sum()
        print(f"Valores nulos: {nulos:,} ({nulos/total_registros*100:.2f}%)")
        
        # Verificar estatísticas básicas
        print("\nEstatísticas de idade:")
        print(f"Mínimo: {df['NU_IDADE_N'].min()}")
        print(f"Máximo: {df['NU_IDADE_N'].max()}")
        print(f"Média: {df['NU_IDADE_N'].mean():.2f}")
        print(f"Mediana: {df['NU_IDADE_N'].median()}")
        
        # Verificar distribuição por faixas etárias
        bins = [0, 5, 15, 30, 45, 60, 150]
        labels = ['0-4', '5-14', '15-29', '30-44', '45-59', '60+']
        
        df['FAIXA_ETARIA'] = pd.cut(
            df['NU_IDADE_N'], 
            bins=bins, 
            labels=labels, 
            right=False
        )
        
        # Contar por faixa etária
        contagem = df['FAIXA_ETARIA'].value_counts().sort_index()
        print("\nContagem por faixa etária:")
        for faixa, count in contagem.items():
            print(f"{faixa}: {count:,} ({count/total_registros*100:.2f}%)")
            
        # Verificar valores únicos no campo de idade
        print("\nPrimeiros 20 valores únicos de idade:")
        print(sorted(df['NU_IDADE_N'].dropna().unique())[:20])
        
        # Verificar se há alguma coluna alternativa de idade
        colunas_idade = [col for col in df.columns if 'IDADE' in col.upper()]
        print("\nColunas relacionadas a idade:", colunas_idade)
        
        # Verificar o campo CS_SEXO
        if 'CS_SEXO' in df.columns:
            sexo_counts = df['CS_SEXO'].value_counts()
            print("\nDistribuição por sexo:")
            for sexo, count in sexo_counts.items():
                print(f"{sexo}: {count:,} ({count/total_registros*100:.2f}%)")
        
    except Exception as e:
        print(f"Erro ao verificar dados: {e}")

if __name__ == "__main__":
    main()
