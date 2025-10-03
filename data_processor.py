#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador de Dados de Dengue - Versão Simplificada
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DengueDataProcessor:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.stats = {}
        
    def load_data(self):
        """
        Carrega o arquivo CSV completo
        """
        print("Carregando dados completos do DENGBR25.csv...")
        print("Este processo pode demorar alguns minutos...")
        
        try:
            self.df = pd.read_csv(self.csv_path, low_memory=False)
            print(f"Dados carregados com sucesso!")
            print(f"Total de registros: {len(self.df):,}")
            print(f"Total de colunas: {len(self.df.columns)}")
            
            self._convert_data_types()
            return True
            
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False
    
    def _convert_data_types(self):
        """
        Converte tipos de dados
        """
        print("Convertendo tipos de dados...")
        
        self.df['SG_UF_NOT'] = self.df['SG_UF_NOT'].astype(str)
        self.df['ID_MUNICIP'] = self.df['ID_MUNICIP'].astype(str)
        self.df['DT_NOTIFIC'] = pd.to_datetime(self.df['DT_NOTIFIC'], errors='coerce')
        self.df['NU_IDADE_N'] = pd.to_numeric(self.df['NU_IDADE_N'], errors='coerce')
        
        print("Conversao concluida!")
    
    def generate_statistics(self):
        """
        Gera estatísticas gerais
        """
        print("Gerando estatisticas...")
        
        # Estatísticas gerais
        self.stats['geral'] = {
            'total_casos': len(self.df),
            'periodo_inicio': str(self.df['DT_NOTIFIC'].min()),
            'periodo_fim': str(self.df['DT_NOTIFIC'].max()),
            'anos_disponiveis': sorted(self.df['NU_ANO'].unique().tolist()),
            'estados_unicos': len(self.df['SG_UF_NOT'].unique())
        }
        
        # Por estado
        casos_por_uf = self.df['SG_UF_NOT'].value_counts().head(20)
        self.stats['por_estado'] = {
            'uf': casos_por_uf.index.tolist(),
            'casos': casos_por_uf.values.tolist()
        }
        
        # Por ano
        casos_por_ano = self.df['NU_ANO'].value_counts().sort_index()
        self.stats['por_ano'] = {
            'anos': casos_por_ano.index.tolist(),
            'casos': casos_por_ano.values.tolist()
        }
        
        # Demográfico
        if 'CS_SEXO' in self.df.columns:
            sexo_dist = self.df['CS_SEXO'].value_counts()
            self.stats['demografico'] = {
                'sexo': {
                    'feminino': int(sexo_dist.get('F', 0)),
                    'masculino': int(sexo_dist.get('M', 0))
                }
            }
        
        # Sintomas
        sintomas = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'EXANTEMA', 'VOMITO', 'NAUSEA']
        sintomas_stats = {}
        for sintoma in sintomas:
            if sintoma in self.df.columns:
                casos_com_sintoma = (self.df[sintoma] == 1).sum()
                sintomas_stats[sintoma.lower()] = {
                    'casos': int(casos_com_sintoma),
                    'percentual': float((casos_com_sintoma / len(self.df)) * 100)
                }
        self.stats['sintomas'] = sintomas_stats
        
        print("Estatisticas geradas!")
    
    def analyze_santa_catarina(self):
        """
        Analisa Santa Catarina
        """
        print("Analisando Santa Catarina...")
        
        sc_data = self.df[self.df['SG_UF_NOT'] == '42']
        
        self.stats['santa_catarina'] = {
            'total_casos': len(sc_data),
            'municipios_afetados': len(sc_data['ID_MUNICIP'].unique()) if len(sc_data) > 0 else 0
        }
        
        if len(sc_data) > 0:
            municipios_sc = sc_data['ID_MUNICIP'].value_counts().head(10)
            self.stats['santa_catarina']['municipios'] = {
                'codigos': municipios_sc.index.tolist(),
                'casos': municipios_sc.values.tolist()
            }
            
            # Criciúma
            criciuma_casos = sc_data[sc_data['ID_MUNICIP'] == '4204608']
            self.stats['santa_catarina']['criciuma'] = {
                'casos': len(criciuma_casos)
            }
        
        print(f"SC: {len(sc_data):,} casos")
    
    def save_statistics(self, output_file='dengue_statistics.json'):
        """
        Salva estatísticas
        """
        print(f"Salvando em {output_file}...")
        
        self.stats['metadata'] = {
            'gerado_em': datetime.now().isoformat(),
            'total_registros': len(self.df)
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
        
        print(f"Salvo em {output_file}")
    
    def process_all(self):
        """
        Processa tudo
        """
        print("INICIANDO PROCESSAMENTO DOS DADOS DE DENGUE")
        print("=" * 50)
        
        if not self.load_data():
            return False
        
        self.generate_statistics()
        self.analyze_santa_catarina()
        self.save_statistics()
        
        print("\nPROCESSAMENTO CONCLUIDO!")
        print("=" * 50)
        
        return True

def main():
    processor = DengueDataProcessor('Documentos/DENGBR25.csv')
    processor.process_all()

if __name__ == "__main__":
    main()
