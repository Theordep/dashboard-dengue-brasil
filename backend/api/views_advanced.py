from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import DengueStatistic
import json
import os

@api_view(['GET'])
def faixas_etarias(request):
    """
    Estatísticas por faixa etária
    """
    try:
        cache_key = 'faixas_etarias'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        try:
            stat = DengueStatistic.objects.get(name='dengue_advanced_statistics')
            data = stat.data.get('faixa_etaria', {})
            
            # Preparar dados para visualização
            faixas = []
            casos = []
            obitos = []
            letalidade = []
            percentuais = []
            
            # Ordenar as faixas etárias corretamente
            ordem_faixas = ['0-4', '5-14', '15-29', '30-44', '45-59', '60+']
            
            for faixa in ordem_faixas:
                if faixa in data:
                    faixas.append(faixa)
                    casos.append(data[faixa]['casos'])
                    obitos.append(data[faixa]['obitos'])
                    letalidade.append(data[faixa]['letalidade'])
                    percentuais.append(data[faixa]['percentual_do_total'])
            
            response_data = {
                'faixas': faixas,
                'casos': casos,
                'obitos': obitos,
                'letalidade': letalidade,
                'percentuais': percentuais,
                'destaques': {
                    'faixa_mais_afetada': max(zip(faixas, casos), key=lambda x: x[1])[0] if casos else None,
                    'faixa_maior_letalidade': max(zip(faixas, letalidade), key=lambda x: x[1])[0] if letalidade else None,
                    'total_casos_criancas': sum([data.get('0-4', {}).get('casos', 0)]) if data else 0,
                    'total_casos_idosos': sum([data.get('60+', {}).get('casos', 0)]) if data else 0
                }
            }
            
            cache.set(cache_key, response_data, 3600)
            return Response(response_data)
            
        except DengueStatistic.DoesNotExist:
            return Response({
                'error': 'Estatísticas avançadas não encontradas. Execute o processador avançado primeiro.'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'error': f'Erro ao buscar dados por faixa etária: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def genero_detalhado(request):
    """
    Estatísticas detalhadas por gênero
    """
    try:
        cache_key = 'genero_detalhado'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        try:
            stat = DengueStatistic.objects.get(name='dengue_advanced_statistics')
            data = stat.data.get('genero_detalhado', {})
            
            # Preparar dados para visualização
            distribuicao_por_faixa = data.get('distribuicao_por_faixa', {})
            sintomas_por_genero = data.get('sintomas_por_genero', {})
            evolucao_por_genero = data.get('evolucao_por_genero', {})
            
            # Calcular alguns destaques
            destaques = {}
            
            # Faixa etária com maior diferença entre gêneros
            maior_diferenca = 0
            faixa_maior_diferenca = None
            
            for faixa, valores in distribuicao_por_faixa.items():
                feminino = valores.get('feminino', 0)
                masculino = valores.get('masculino', 0)
                diferenca = abs(feminino - masculino)
                
                if diferenca > maior_diferenca:
                    maior_diferenca = diferenca
                    faixa_maior_diferenca = faixa
            
            destaques['faixa_maior_diferenca'] = faixa_maior_diferenca
            
            # Sintoma com maior diferença percentual entre gêneros
            maior_dif_sintoma = 0
            sintoma_maior_diferenca = None
            
            sintomas_fem = sintomas_por_genero.get('feminino', {})
            sintomas_masc = sintomas_por_genero.get('masculino', {})
            
            for sintoma in sintomas_fem:
                if sintoma in sintomas_masc:
                    perc_fem = sintomas_fem[sintoma].get('percentual', 0)
                    perc_masc = sintomas_masc[sintoma].get('percentual', 0)
                    dif_sintoma = abs(perc_fem - perc_masc)
                    
                    if dif_sintoma > maior_dif_sintoma:
                        maior_dif_sintoma = dif_sintoma
                        sintoma_maior_diferenca = sintoma
            
            destaques['sintoma_maior_diferenca'] = sintoma_maior_diferenca
            
            # Diferença na letalidade
            letalidade_fem = evolucao_por_genero.get('feminino', {}).get('obito', {}).get('percentual', 0)
            letalidade_masc = evolucao_por_genero.get('masculino', {}).get('obito', {}).get('percentual', 0)
            
            destaques['letalidade'] = {
                'feminino': letalidade_fem,
                'masculino': letalidade_masc,
                'diferenca': abs(letalidade_fem - letalidade_masc)
            }
            
            response_data = {
                'distribuicao_por_faixa': distribuicao_por_faixa,
                'sintomas_por_genero': sintomas_por_genero,
                'evolucao_por_genero': evolucao_por_genero,
                'destaques': destaques
            }
            
            cache.set(cache_key, response_data, 3600)
            return Response(response_data)
            
        except DengueStatistic.DoesNotExist:
            return Response({
                'error': 'Estatísticas avançadas não encontradas. Execute o processador avançado primeiro.'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'error': f'Erro ao buscar dados detalhados por gênero: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def santa_catarina_avancado(request):
    """
    Estatísticas avançadas para Santa Catarina
    """
    try:
        cache_key = 'santa_catarina_avancado'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        try:
            stat = DengueStatistic.objects.get(name='dengue_advanced_statistics')
            data = stat.data.get('santa_catarina', {})
            
            # Adicionar dados de municípios com seus nomes
            municipios_data = data.get('municipios', {})
            codigos = municipios_data.get('codigos', [])
            casos = municipios_data.get('casos', [])
            
            # Mapeamento de códigos para nomes (simplificado)
            # Em uma implementação real, isso viria do banco de dados
            nomes_municipios = {
                '420540': 'Florianópolis',
                '420820': 'Joinville',
                '420200': 'Blumenau',
                '420420': 'Balneário Camboriú',
                '420910': 'Lages',
                '420830': 'Jaraguá do Sul',
                '421660': 'São José',
                '421720': 'São Miguel do Oeste',
                '420240': 'Brusque',
                '420890': 'Itajaí',
                '420460': 'Criciúma'
            }
            
            # Adicionar nomes dos municípios
            nomes = []
            for codigo in codigos:
                nome = nomes_municipios.get(codigo, f'Município {codigo}')
                nomes.append(nome)
            
            municipios = {
                'codigos': codigos,
                'nomes': nomes,
                'casos': casos
            }
            
            # Análise temporal
            analise_temporal = data.get('analise_temporal', {})
            
            # Comparação nacional
            comparacao_nacional = data.get('comparacao_nacional', {})
            
            # Destaques para SC
            destaques = {
                'municipio_mais_casos': nomes[0] if nomes else None,
                'percentual_do_total_nacional': comparacao_nacional.get('percentual_do_total', 0),
                'incidencia_vs_nacional': comparacao_nacional.get('razao_incidencia', 0),
                'maior_crescimento_mensal': max(analise_temporal.get('crescimento_percentual', [0])) if analise_temporal else 0
            }
            
            response_data = {
                'total_casos': data.get('total_casos', 0),
                'municipios_afetados': data.get('municipios_afetados', 0),
                'municipios': municipios,
                'analise_temporal': analise_temporal,
                'comparacao_nacional': comparacao_nacional,
                'destaques': destaques,
                'criciuma': data.get('criciuma', {})
            }
            
            cache.set(cache_key, response_data, 3600)
            return Response(response_data)
            
        except DengueStatistic.DoesNotExist:
            return Response({
                'error': 'Estatísticas avançadas não encontradas. Execute o processador avançado primeiro.'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'error': f'Erro ao buscar dados avançados de Santa Catarina: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def sintomas_por_perfil(request):
    """
    Estatísticas de sintomas por perfil (idade e gênero)
    """
    try:
        cache_key = 'sintomas_por_perfil'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        try:
            stat = DengueStatistic.objects.get(name='dengue_advanced_statistics')
            data = stat.data.get('sintomas_por_perfil', {})
            
            # Sintomas por faixa etária
            por_faixa_etaria = data.get('por_faixa_etaria', {})
            
            # Combinações mais comuns
            combinacoes_mais_comuns = data.get('combinacoes_mais_comuns', [])
            
            # Encontrar sintoma mais comum por faixa etária
            sintoma_mais_comum = {}
            for faixa, sintomas in por_faixa_etaria.items():
                max_percentual = 0
                sintoma_max = None
                
                for sintoma, valores in sintomas.items():
                    percentual = valores.get('percentual', 0)
                    if percentual > max_percentual:
                        max_percentual = percentual
                        sintoma_max = sintoma
                
                if sintoma_max:
                    sintoma_mais_comum[faixa] = {
                        'sintoma': sintoma_max,
                        'percentual': max_percentual
                    }
            
            # Destaques
            destaques = {
                'sintoma_mais_comum_criancas': sintoma_mais_comum.get('0-4', {}).get('sintoma', 'N/A'),
                'sintoma_mais_comum_idosos': sintoma_mais_comum.get('60+', {}).get('sintoma', 'N/A'),
                'combinacao_mais_comum': combinacoes_mais_comuns[0]['sintomas'] if combinacoes_mais_comuns else []
            }
            
            response_data = {
                'por_faixa_etaria': por_faixa_etaria,
                'combinacoes_mais_comuns': combinacoes_mais_comuns,
                'sintoma_mais_comum_por_faixa': sintoma_mais_comum,
                'destaques': destaques
            }
            
            cache.set(cache_key, response_data, 3600)
            return Response(response_data)
            
        except DengueStatistic.DoesNotExist:
            return Response({
                'error': 'Estatísticas avançadas não encontradas. Execute o processador avançado primeiro.'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'error': f'Erro ao buscar dados de sintomas por perfil: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def carregar_estatisticas_avancadas(request):
    """
    Carrega estatísticas avançadas do arquivo JSON
    """
    try:
        json_file = 'dengue_advanced_statistics.json'
        
        if not os.path.exists(json_file):
            return Response({
                'error': f'Arquivo {json_file} não encontrado. Execute o processador avançado primeiro.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Salvar no banco de dados
        stat, created = DengueStatistic.objects.update_or_create(
            name='dengue_advanced_statistics',
            defaults={'data': data}
        )
        
        # Limpar cache
        cache.delete('faixas_etarias')
        cache.delete('genero_detalhado')
        cache.delete('santa_catarina_avancado')
        cache.delete('sintomas_por_perfil')
        
        return Response({
            'message': 'Estatísticas avançadas carregadas com sucesso!',
            'created': created
        })
        
    except Exception as e:
        return Response({
            'error': f'Erro ao carregar estatísticas avançadas: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
