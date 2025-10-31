#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador Avançado de Dados de Dengue
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DengueAdvancedProcessor:
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
        
        # Converter ANO_NASC para numérico
        self.df['ANO_NASC'] = pd.to_numeric(self.df['ANO_NASC'], errors='coerce')
        
        # Calcular idade em anos a partir do ANO_NASC e ano da notificação
        if 'ANO_NASC' in self.df.columns and 'NU_ANO' in self.df.columns:
            # Calcular idade aproximada: ano da notificação - ano de nascimento
            self.df['IDADE_ANOS'] = self.df['NU_ANO'] - self.df['ANO_NASC']
            # Filtrar idades inválidas (negativas, muito altas)
            self.df['IDADE_ANOS'] = self.df['IDADE_ANOS'].apply(
                lambda x: x if pd.notna(x) and 0 <= x <= 120 else pd.NA
            )
            print(f"Idade calculada para {self.df['IDADE_ANOS'].notna().sum():,} registros")
        else:
            # Fallback: tentar usar NU_IDADE_N se disponível (pode estar em dias, converter para anos)
            self.df['NU_IDADE_N'] = pd.to_numeric(self.df['NU_IDADE_N'], errors='coerce')
            # Se os valores são muito grandes (> 1000), pode estar em dias
            if self.df['NU_IDADE_N'].notna().any():
                max_val = self.df['NU_IDADE_N'].max()
                if max_val > 1000:
                    # Provavelmente está em dias, converter para anos aproximados
                    self.df['IDADE_ANOS'] = (self.df['NU_IDADE_N'] / 365.25).round().astype('Int64')
                    self.df['IDADE_ANOS'] = self.df['IDADE_ANOS'].apply(
                        lambda x: x if pd.notna(x) and 0 <= x <= 120 else pd.NA
                    )
                else:
                    # Usar diretamente se parece estar em anos
                    self.df['IDADE_ANOS'] = self.df['NU_IDADE_N'].apply(
                        lambda x: x if pd.notna(x) and 0 <= x <= 120 else pd.NA
                    )
        
        # Adicionar coluna de mês para análises temporais
        self.df['MES'] = self.df['DT_NOTIFIC'].dt.month
        
        print("Conversão concluída!")
    
    def _categorize_age_groups(self):
        """
        Categoriza faixas etárias
        """
        bins = [0, 5, 15, 30, 45, 60, 150]
        labels = ['0-4', '5-14', '15-29', '30-44', '45-59', '60+']
        
        # Usar IDADE_ANOS calculada ao invés de NU_IDADE_N
        if 'IDADE_ANOS' not in self.df.columns:
            print("ERRO: Coluna IDADE_ANOS nao encontrada!")
            return None
        
        # Inicializar com NaN
        self.df['FAIXA_ETARIA'] = pd.NA
        
        # Filtrar apenas registros com idade válida
        mask_idade_valida = self.df['IDADE_ANOS'].notna()
        
        if mask_idade_valida.any():
            self.df.loc[mask_idade_valida, 'FAIXA_ETARIA'] = pd.cut(
                self.df.loc[mask_idade_valida, 'IDADE_ANOS'], 
                bins=bins, 
                labels=labels, 
                right=False
            )
        
        return self.df['FAIXA_ETARIA']
    
    def generate_basic_statistics(self):
        """
        Gera estatísticas básicas (similar ao data_processor_simple.py)
        """
        print("Gerando estatísticas básicas...")
        
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
        
        # Demográfico básico
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
        
        print("Estatísticas básicas geradas!")
    
    def analyze_age_groups(self):
        """
        Análise detalhada por faixa etária
        """
        print("Analisando faixas etárias...")
        
        # Categorizar faixas etárias
        self._categorize_age_groups()
        
        # Garantir que todas as faixas etárias estejam presentes, mesmo com 0 casos
        todas_faixas = ['0-4', '5-14', '15-29', '30-44', '45-59', '60+']
        
        # Contagem por faixa etária (incluindo NaN)
        age_counts = self.df['FAIXA_ETARIA'].value_counts().sort_index()
        
        # Calcular letalidade por faixa etária (evolução = 2 é óbito por dengue)
        letalidade_por_faixa = {}
        
        # Processar todas as faixas, garantindo que todas estejam no resultado
        for faixa in todas_faixas:
            casos_faixa = self.df[self.df['FAIXA_ETARIA'] == faixa]
            total_casos = len(casos_faixa)
            
            # Verificar se EVOLUCAO está presente
            if 'EVOLUCAO' in self.df.columns and total_casos > 0:
                obitos = len(casos_faixa[casos_faixa['EVOLUCAO'] == 2])
                taxa_letalidade = (obitos / total_casos * 100) if total_casos > 0 else 0
            else:
                obitos = 0
                taxa_letalidade = 0
            
            letalidade_por_faixa[faixa] = {
                'casos': int(total_casos),
                'obitos': int(obitos),
                'letalidade': float(taxa_letalidade),
                'percentual_do_total': float(total_casos / len(self.df) * 100) if len(self.df) > 0 else 0
            }
        
        # Adicionar informações sobre dados faltantes
        dados_com_idade = self.df['FAIXA_ETARIA'].notna().sum()
        dados_sem_idade = len(self.df) - dados_com_idade
        
        if dados_sem_idade > 0:
            print(f"ATENCAO: {dados_sem_idade:,} registros ({dados_sem_idade/len(self.df)*100:.2f}%) nao tem idade valida!")
        
        self.stats['faixa_etaria'] = letalidade_por_faixa
        print("Análise de faixas etárias concluída!")
    
    def analyze_gender_details(self):
        """
        Análise detalhada por gênero
        """
        print("Analisando detalhes por gênero...")
        
        if 'CS_SEXO' not in self.df.columns:
            print("Dados de gênero não disponíveis!")
            return
        
        # Filtrar apenas M e F, ignorando valores inválidos
        df_genero = self.df[self.df['CS_SEXO'].isin(['M', 'F'])]
        
        # Distribuição por faixa etária e gênero
        self._categorize_age_groups()  # Garantir que as faixas etárias estão categorizadas
        
        genero_por_faixa = {}
        for faixa in df_genero['FAIXA_ETARIA'].unique():
            if pd.isna(faixa):
                continue
                
            casos_faixa = df_genero[df_genero['FAIXA_ETARIA'] == faixa]
            genero_counts = casos_faixa['CS_SEXO'].value_counts()
            
            genero_por_faixa[faixa] = {
                'feminino': int(genero_counts.get('F', 0)),
                'masculino': int(genero_counts.get('M', 0))
            }
        
        # Sintomas mais comuns por gênero
        sintomas = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'EXANTEMA', 'VOMITO', 'NAUSEA']
        sintomas_por_genero = {'feminino': {}, 'masculino': {}}
        
        for sintoma in sintomas:
            if sintoma not in self.df.columns:
                continue
                
            # Feminino
            df_fem = df_genero[df_genero['CS_SEXO'] == 'F']
            casos_sintoma_fem = (df_fem[sintoma] == 1).sum()
            perc_fem = (casos_sintoma_fem / len(df_fem) * 100) if len(df_fem) > 0 else 0
            
            sintomas_por_genero['feminino'][sintoma.lower()] = {
                'casos': int(casos_sintoma_fem),
                'percentual': float(perc_fem)
            }
            
            # Masculino
            df_masc = df_genero[df_genero['CS_SEXO'] == 'M']
            casos_sintoma_masc = (df_masc[sintoma] == 1).sum()
            perc_masc = (casos_sintoma_masc / len(df_masc) * 100) if len(df_masc) > 0 else 0
            
            sintomas_por_genero['masculino'][sintoma.lower()] = {
                'casos': int(casos_sintoma_masc),
                'percentual': float(perc_masc)
            }
        
        # Evolução clínica por gênero
        evolucao_por_genero = {'feminino': {}, 'masculino': {}}
        
        if 'EVOLUCAO' in self.df.columns:
            # Feminino
            df_fem = df_genero[df_genero['CS_SEXO'] == 'F']
            evolucao_fem = df_fem['EVOLUCAO'].value_counts()
            
            # Cura (1)
            cura_fem = evolucao_fem.get(1, 0)
            perc_cura_fem = (cura_fem / len(df_fem) * 100) if len(df_fem) > 0 else 0
            
            # Óbito por dengue (2)
            obito_fem = evolucao_fem.get(2, 0)
            perc_obito_fem = (obito_fem / len(df_fem) * 100) if len(df_fem) > 0 else 0
            
            evolucao_por_genero['feminino'] = {
                'cura': {
                    'casos': int(cura_fem),
                    'percentual': float(perc_cura_fem)
                },
                'obito': {
                    'casos': int(obito_fem),
                    'percentual': float(perc_obito_fem)
                }
            }
            
            # Masculino
            df_masc = df_genero[df_genero['CS_SEXO'] == 'M']
            evolucao_masc = df_masc['EVOLUCAO'].value_counts()
            
            # Cura (1)
            cura_masc = evolucao_masc.get(1, 0)
            perc_cura_masc = (cura_masc / len(df_masc) * 100) if len(df_masc) > 0 else 0
            
            # Óbito por dengue (2)
            obito_masc = evolucao_masc.get(2, 0)
            perc_obito_masc = (obito_masc / len(df_masc) * 100) if len(df_masc) > 0 else 0
            
            evolucao_por_genero['masculino'] = {
                'cura': {
                    'casos': int(cura_masc),
                    'percentual': float(perc_cura_masc)
                },
                'obito': {
                    'casos': int(obito_masc),
                    'percentual': float(perc_obito_masc)
                }
            }
        
        # Consolidar estatísticas de gênero
        self.stats['genero_detalhado'] = {
            'distribuicao_por_faixa': genero_por_faixa,
            'sintomas_por_genero': sintomas_por_genero,
            'evolucao_por_genero': evolucao_por_genero
        }
        
        print("Análise detalhada por gênero concluída!")
    
    def analyze_santa_catarina_details(self):
        """
        Análise detalhada para Santa Catarina
        """
        print("Analisando Santa Catarina detalhadamente...")
        
        # Filtrar dados de SC
        sc_data = self.df[self.df['SG_UF_NOT'] == '42']
        
        # Estatísticas básicas
        self.stats['santa_catarina'] = {
            'total_casos': len(sc_data),
            'municipios_afetados': len(sc_data['ID_MUNICIP'].unique()) if len(sc_data) > 0 else 0
        }
        
        if len(sc_data) > 0:
            # Top 10 municípios
            municipios_sc = sc_data['ID_MUNICIP'].value_counts().head(10)
            self.stats['santa_catarina']['municipios'] = {
                'codigos': municipios_sc.index.tolist(),
                'casos': municipios_sc.values.tolist()
            }
            
            # Criciúma
            criciuma_casos = sc_data[sc_data['ID_MUNICIP'] == '420460']
            self.stats['santa_catarina']['criciuma'] = {
                'casos': len(criciuma_casos)
            }
            
            # Análise temporal (mês a mês)
            if 'MES' in sc_data.columns:
                casos_por_mes = sc_data['MES'].value_counts().sort_index()
                
                # Calcular crescimento percentual mês a mês
                crescimento_mensal = []
                meses = casos_por_mes.index.tolist()
                casos = casos_por_mes.values.tolist()
                
                for i in range(1, len(meses)):
                    mes_anterior = casos[i-1]
                    mes_atual = casos[i]
                    
                    if mes_anterior > 0:
                        crescimento = ((mes_atual - mes_anterior) / mes_anterior) * 100
                    else:
                        crescimento = 0
                        
                    crescimento_mensal.append(float(crescimento))
                
                self.stats['santa_catarina']['analise_temporal'] = {
                    'meses': meses,
                    'casos': casos,
                    'crescimento_percentual': [0] + crescimento_mensal  # Primeiro mês não tem crescimento
                }
            
            # Comparação com média nacional
            total_nacional = len(self.df)
            casos_sc = len(sc_data)
            
            # Percentual de SC em relação ao total nacional
            percentual_sc = (casos_sc / total_nacional * 100) if total_nacional > 0 else 0
            
            # Calcular população estimada de SC (aproximadamente 7 milhões) e do Brasil (212 milhões)
            # Estes são valores aproximados para cálculo de incidência
            pop_sc = 7000000
            pop_br = 212000000
            
            # Taxa de incidência por 100k habitantes
            incidencia_sc = (casos_sc / pop_sc) * 100000
            incidencia_br = (total_nacional / pop_br) * 100000
            
            self.stats['santa_catarina']['comparacao_nacional'] = {
                'percentual_do_total': float(percentual_sc),
                'incidencia_por_100k': float(incidencia_sc),
                'incidencia_nacional_por_100k': float(incidencia_br),
                'razao_incidencia': float(incidencia_sc / incidencia_br) if incidencia_br > 0 else 0
            }
        
        print("Análise detalhada de Santa Catarina concluída!")
    
    def analyze_symptoms_by_profile(self):
        """
        Análise de sintomas por perfil (idade e gênero)
        """
        print("Analisando sintomas por perfil...")
        
        sintomas = ['FEBRE', 'MIALGIA', 'CEFALEIA', 'EXANTEMA', 'VOMITO', 'NAUSEA']
        
        # Verificar se temos os dados necessários
        if not all(sintoma in self.df.columns for sintoma in sintomas):
            print("Dados de sintomas incompletos!")
            return
        
        # Categorizar faixas etárias se ainda não foi feito
        if 'FAIXA_ETARIA' not in self.df.columns:
            self._categorize_age_groups()
        
        # Garantir que todas as faixas etárias estejam presentes
        todas_faixas = ['0-4', '5-14', '15-29', '30-44', '45-59', '60+']
        
        # Sintomas por faixa etária
        sintomas_por_faixa = {}
        
        # Processar todas as faixas, mesmo as sem dados
        for faixa in todas_faixas:
            df_faixa = self.df[self.df['FAIXA_ETARIA'] == faixa]
            sintomas_faixa = {}
            
            for sintoma in sintomas:
                casos_sintoma = (df_faixa[sintoma] == 1).sum() if len(df_faixa) > 0 else 0
                perc_sintoma = (casos_sintoma / len(df_faixa) * 100) if len(df_faixa) > 0 else 0
                
                sintomas_faixa[sintoma.lower()] = {
                    'casos': int(casos_sintoma),
                    'percentual': float(perc_sintoma)
                }
            
            sintomas_por_faixa[faixa] = sintomas_faixa
        
        # Combinações de sintomas mais frequentes
        # Vamos analisar as combinações de 2 sintomas mais comuns
        combinacoes = []
        
        for i in range(len(sintomas)):
            for j in range(i+1, len(sintomas)):
                sintoma1 = sintomas[i]
                sintoma2 = sintomas[j]
                
                # Casos com ambos os sintomas
                casos_combinados = ((self.df[sintoma1] == 1) & (self.df[sintoma2] == 1)).sum()
                
                if casos_combinados > 0:
                    perc_combinados = (casos_combinados / len(self.df)) * 100
                    
                    combinacoes.append({
                        'sintomas': [sintoma1.lower(), sintoma2.lower()],
                        'casos': int(casos_combinados),
                        'percentual': float(perc_combinados)
                    })
        
        # Ordenar combinações por número de casos (decrescente)
        combinacoes.sort(key=lambda x: x['casos'], reverse=True)
        
        # Pegar as 5 combinações mais comuns
        top_combinacoes = combinacoes[:5]
        
        self.stats['sintomas_por_perfil'] = {
            'por_faixa_etaria': sintomas_por_faixa,
            'combinacoes_mais_comuns': top_combinacoes
        }
        
        print("Análise de sintomas por perfil concluída!")
    
    def save_statistics(self, output_file='dengue_advanced_statistics.json'):
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
        print("INICIANDO PROCESSAMENTO AVANÇADO DOS DADOS DE DENGUE")
        print("=" * 50)
        
        if not self.load_data():
            return False
        
        # Gerar estatísticas básicas (compatíveis com o processador simples)
        self.generate_basic_statistics()
        
        # Gerar estatísticas avançadas
        self.analyze_age_groups()
        self.analyze_gender_details()
        self.analyze_santa_catarina_details()
        self.analyze_symptoms_by_profile()
        
        self.save_statistics()
        
        print("\nPROCESSAMENTO AVANÇADO CONCLUÍDO!")
        print("=" * 50)
        
        return True

def main():
    processor = DengueAdvancedProcessor('Documentos/DENGBR25.csv')
    processor.process_all()

if __name__ == "__main__":
    main()
