#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador de Dados de Dengue - Carregamento Completo
Script para processar o arquivo DENGBR25.csv completo e preparar para o dashboard
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
        print("Este processo pode demorar alguns minutos devido ao tamanho do arquivo...")
        
        try:
            # Carregar dados completos
            self.df = pd.read_csv(self.csv_path, low_memory=False)
            print(f"Dados carregados com sucesso!")
            print(f"Total de registros: {len(self.df):,}")
            print(f"Total de colunas: {len(self.df.columns)}")
            
            # Converter tipos de dados
            self._convert_data_types()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return False
    
    def _convert_data_types(self):
        """
        Converte tipos de dados para otimizar processamento
        """
        print("Convertendo tipos de dados...")
        
        # Converter códigos para string
        self.df['SG_UF_NOT'] = self.df['SG_UF_NOT'].astype(str)
        self.df['ID_MUNICIP'] = self.df['ID_MUNICIP'].astype(str)
        
        # Converter datas
        self.df['DT_NOTIFIC'] = pd.to_datetime(self.df['DT_NOTIFIC'], errors='coerce')
        self.df['DT_SIN_PRI'] = pd.to_datetime(self.df['DT_SIN_PRI'], errors='coerce')
        
        # Converter idade para numérico
        self.df['NU_IDADE_N'] = pd.to_numeric(self.df['NU_IDADE_N'], errors='coerce')
        
        print("✅ Conversão de tipos concluída!")
    
    def generate_statistics(self):
        """
        Gera estatísticas gerais dos dados
        """
        print("📊 Gerando estatísticas...")
        
        # Estatísticas gerais
        self.stats['geral'] = {
            'total_casos': len(self.df),
            'periodo_inicio': str(self.df['DT_NOTIFIC'].min()),
            'periodo_fim': str(self.df['DT_NOTIFIC'].max()),
            'anos_disponiveis': sorted(self.df['NU_ANO'].unique().tolist()),
            'estados_unicos': len(self.df['SG_UF_NOT'].unique()),
            'municipios_unicos': len(self.df['ID_MUNICIP'].unique())
        }
        
        # Estatísticas por estado
        casos_por_uf = self.df['SG_UF_NOT'].value_counts().head(20)
        self.stats['por_estado'] = {
            'uf': casos_por_uf.index.tolist(),
            'casos': casos_por_uf.values.tolist(),
            'percentual': (casos_por_uf.values / len(self.df) * 100).tolist()
        }
        
        # Estatísticas por ano
        casos_por_ano = self.df['NU_ANO'].value_counts().sort_index()
        self.stats['por_ano'] = {
            'anos': casos_por_ano.index.tolist(),
            'casos': casos_por_ano.values.tolist()
        }
        
        # Estatísticas por mês
        self.df['MES'] = self.df['DT_NOTIFIC'].dt.month
        casos_por_mes = self.df.groupby('MES').size()
        meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                      'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        self.stats['por_mes'] = {
            'meses': [meses_nomes[int(i)-1] for i in casos_por_mes.index if not pd.isna(i)],
            'casos': [casos_por_mes[i] for i in casos_por_mes.index if not pd.isna(i)]
        }
        
        # Estatísticas demográficas
        if 'CS_SEXO' in self.df.columns:
            sexo_dist = self.df['CS_SEXO'].value_counts()
            self.stats['demografico'] = {
                'sexo': {
                    'feminino': int(sexo_dist.get('F', 0)),
                    'masculino': int(sexo_dist.get('M', 0)),
                    'ignorado': int(sexo_dist.get('I', 0))
                }
            }
        
        # Estatísticas de idade
        idades_validas = self.df['NU_IDADE_N'].notna()
        if idades_validas.sum() > 0:
            self.stats['demografico']['idade'] = {
                'media': float(self.df['NU_IDADE_N'].mean()),
                'mediana': float(self.df['NU_IDADE_N'].median()),
                'minima': float(self.df['NU_IDADE_N'].min()),
                'maxima': float(self.df['NU_IDADE_N'].max())
            }
        
        # Sintomas mais comuns
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
        
        # Classificação final
        if 'CLASSI_FIN' in self.df.columns:
            classif_dist = self.df['CLASSI_FIN'].value_counts()
            self.stats['classificacao'] = {
                'confirmado': int(classif_dist.get(10.0, 0)),
                'descartado': int(classif_dist.get(8.0, 0)),
                'inconclusivo': int(classif_dist.get(11.0, 0)),
                'obito_dengue': int(classif_dist.get(12.0, 0))
            }
        
        # Evolução dos casos
        if 'EVOLUCAO' in self.df.columns:
            evol_dist = self.df['EVOLUCAO'].value_counts()
            self.stats['evolucao'] = {
                'cura': int(evol_dist.get(1.0, 0)),
                'obito_dengue': int(evol_dist.get(2.0, 0)),
                'obito_outras': int(evol_dist.get(3.0, 0)),
                'obito_investigacao': int(evol_dist.get(4.0, 0)),
                'ignorado': int(evol_dist.get(9.0, 0))
            }
        
        print("✅ Estatísticas geradas com sucesso!")
    
    def analyze_santa_catarina(self):
        """
        Análise específica de Santa Catarina
        """
        print("🏙️ Analisando dados de Santa Catarina...")
        
        # Filtrar dados de SC
        sc_data = self.df[self.df['SG_UF_NOT'] == '42']
        
        if len(sc_data) == 0:
            print("⚠️  Nenhum caso encontrado em Santa Catarina")
            self.stats['santa_catarina'] = {'total_casos': 0}
            return
        
        # Estatísticas de SC
        self.stats['santa_catarina'] = {
            'total_casos': len(sc_data),
            'municipios_afetados': len(sc_data['ID_MUNICIP'].unique()),
            'periodo_inicio': str(sc_data['DT_NOTIFIC'].min()),
            'periodo_fim': str(sc_data['DT_NOTIFIC'].max())
        }
        
        # Municípios de SC com mais casos
        municipios_sc = sc_data['ID_MUNICIP'].value_counts().head(10)
        self.stats['santa_catarina']['municipios'] = {
            'codigos': municipios_sc.index.tolist(),
            'casos': municipios_sc.values.tolist()
        }
        
        # Verificar Criciúma especificamente
        criciuma_casos = sc_data[sc_data['ID_MUNICIP'] == '4204608']
        self.stats['santa_catarina']['criciuma'] = {
            'casos': len(criciuma_casos),
            'periodo': str(criciuma_casos['DT_NOTIFIC'].min()) if len(criciuma_casos) > 0 else None
        }
        
        print(f"✅ SC analisado: {len(sc_data):,} casos em {len(sc_data['ID_MUNICIP'].unique())} municípios")
        if len(criciuma_casos) > 0:
            print(f"🏙️ Criciúma: {len(criciuma_casos)} casos")
    
    def generate_trends(self):
        """
        Gera análises de tendências temporais
        """
        print("📈 Gerando análises de tendências...")
        
        # Tendência mensal
        self.df['ANO_MES'] = self.df['DT_NOTIFIC'].dt.to_period('M')
        tendencia_mensal = self.df.groupby('ANO_MES').size().reset_index(name='casos')
        
        self.stats['tendencias'] = {
            'mensal': {
                'periodos': [str(period) for period in tendencia_mensal['ANO_MES']],
                'casos': tendencia_mensal['casos'].tolist()
            }
        }
        
        # Sazonalidade (agregando por mês independente do ano)
        sazonalidade = self.df.groupby('MES').size()
        meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                      'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        self.stats['tendencias']['sazonalidade'] = {
            'meses': [meses_nomes[int(i)-1] for i in sazonalidade.index if not pd.isna(i)],
            'casos_medio': [int(sazonalidade[i]) for i in sazonalidade.index if not pd.isna(i)]
        }
        
        print("✅ Tendências geradas com sucesso!")
    
    def save_statistics(self, output_file='dengue_statistics.json'):
        """
        Salva as estatísticas em arquivo JSON
        """
        print(f"💾 Salvando estatísticas em {output_file}...")
        
        # Adicionar metadados
        self.stats['metadata'] = {
            'gerado_em': datetime.now().isoformat(),
            'fonte': 'DATASUS - DENGBR25.csv',
            'total_registros_processados': len(self.df)
        }
        
        # Salvar em JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Estatísticas salvas em {output_file}")
    
    def get_sample_data(self, n=1000):
        """
        Retorna uma amostra dos dados para testes
        """
        sample = self.df.sample(n=n, random_state=42)
        return sample.to_dict('records')
    
    def process_all(self):
        """
        Executa todo o processamento
        """
        print("🚀 INICIANDO PROCESSAMENTO COMPLETO DOS DADOS DE DENGUE")
        print("=" * 60)
        
        # Carregar dados
        if not self.load_data():
            return False
        
        # Gerar estatísticas
        self.generate_statistics()
        
        # Analisar Santa Catarina
        self.analyze_santa_catarina()
        
        # Gerar tendências
        self.generate_trends()
        
        # Salvar resultados
        self.save_statistics()
        
        print("\n🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print(f"📊 Total de registros processados: {len(self.df):,}")
        print(f"📁 Estatísticas salvas em: dengue_statistics.json")
        
        return True

def main():
    """
    Função principal
    """
    processor = DengueDataProcessor('Documentos/DENGBR25.csv')
    processor.process_all()

if __name__ == "__main__":
    main()
