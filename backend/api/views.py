from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.cache import cache
from .models import DengueStatistic, Estado, Municipio, CasoDengue
import json
import os
from datetime import datetime, timedelta

# Códigos de UF para nomes
UF_CODES = {
    '11': 'Rondônia', '12': 'Acre', '13': 'Amazonas', '14': 'Roraima', '15': 'Pará',
    '16': 'Amapá', '17': 'Tocantins', '21': 'Maranhão', '22': 'Piauí', '23': 'Ceará',
    '24': 'Rio Grande do Norte', '25': 'Paraíba', '26': 'Pernambuco', '27': 'Alagoas',
    '28': 'Sergipe', '29': 'Bahia', '31': 'Minas Gerais', '32': 'Espírito Santo',
    '33': 'Rio de Janeiro', '35': 'São Paulo', '41': 'Paraná', '42': 'Santa Catarina',
    '43': 'Rio Grande do Sul', '50': 'Mato Grosso do Sul', '51': 'Mato Grosso',
    '52': 'Goiás', '53': 'Distrito Federal'
}

@api_view(['GET'])
def dashboard_overview(request):
    """
    Endpoint principal do dashboard com visão geral
    """
    try:
        # Tentar buscar do cache primeiro
        cache_key = 'dashboard_overview'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        # Se não estiver em cache, buscar das estatísticas
        try:
            stat = DengueStatistic.objects.get(name='dengue_statistics')
            data = stat.data
            
            # Preparar resposta
            response_data = {
                'geral': data.get('geral', {}),
                'por_estado': data.get('por_estado', {}),
                'demografico': data.get('demografico', {}),
                'sintomas': data.get('sintomas', {}),
                'santa_catarina': data.get('santa_catarina', {}),
                'metadata': data.get('metadata', {})
            }
            
            # Cache por 1 hora
            cache.set(cache_key, response_data, 3600)
            
            return Response(response_data)
            
        except DengueStatistic.DoesNotExist:
            return Response({
                'error': 'Dados não encontrados. Execute o processamento dos dados primeiro.'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'error': f'Erro interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def estatisticas_por_estado(request):
    """
    Estatísticas detalhadas por estado
    """
    try:
        cache_key = 'estatisticas_por_estado'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        stat = DengueStatistic.objects.get(name='dengue_statistics')
        data = stat.data.get('por_estado', {})
        
        # Adicionar nomes dos estados
        estados_com_nomes = []
        for i, uf in enumerate(data.get('uf', [])):
            estados_com_nomes.append({
                'codigo': uf,
                'nome': UF_CODES.get(uf, f'UF {uf}'),
                'casos': data.get('casos', [])[i] if i < len(data.get('casos', [])) else 0,
                'percentual': data.get('percentual', [])[i] if i < len(data.get('percentual', [])) else 0
            })
        
        response_data = {
            'estados': estados_com_nomes,
            'total_estados': len(estados_com_nomes)
        }
        
        cache.set(cache_key, response_data, 3600)
        return Response(response_data)
        
    except Exception as e:
        return Response({
            'error': f'Erro ao buscar dados por estado: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def estatisticas_por_ano(request):
    """
    Estatísticas por ano
    """
    try:
        cache_key = 'estatisticas_por_ano'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        stat = DengueStatistic.objects.get(name='dengue_statistics')
        data = stat.data.get('por_ano', {})
        
        response_data = {
            'anos': data.get('anos', []),
            'casos': data.get('casos', []),
            'total_anos': len(data.get('anos', []))
        }
        
        cache.set(cache_key, response_data, 3600)
        return Response(response_data)
        
    except Exception as e:
        return Response({
            'error': f'Erro ao buscar dados por ano: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def sintomas_mais_comuns(request):
    """
    Lista dos sintomas mais comuns
    """
    try:
        cache_key = 'sintomas_mais_comuns'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        stat = DengueStatistic.objects.get(name='dengue_statistics')
        sintomas_data = stat.data.get('sintomas', {})
        
        # Converter para lista ordenada
        sintomas_lista = []
        for sintoma, dados in sintomas_data.items():
            sintomas_lista.append({
                'nome': sintoma.upper(),
                'casos': dados.get('casos', 0),
                'percentual': dados.get('percentual', 0)
            })
        
        # Ordenar por número de casos
        sintomas_lista.sort(key=lambda x: x['casos'], reverse=True)
        
        response_data = {
            'sintomas': sintomas_lista,
            'total_sintomas': len(sintomas_lista)
        }
        
        cache.set(cache_key, response_data, 3600)
        return Response(response_data)
        
    except Exception as e:
        return Response({
            'error': f'Erro ao buscar sintomas: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def santa_catarina_detalhes(request):
    """
    Detalhes específicos de Santa Catarina
    """
    try:
        cache_key = 'santa_catarina_detalhes'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        stat = DengueStatistic.objects.get(name='dengue_statistics')
        sc_data = stat.data.get('santa_catarina', {})
        
        response_data = {
            'total_casos': sc_data.get('total_casos', 0),
            'municipios_afetados': sc_data.get('municipios_afetados', 0),
            'municipios': sc_data.get('municipios', {}),
            'criciuma': sc_data.get('criciuma', {}),
            'analise': {
                'tem_dados': sc_data.get('total_casos', 0) > 0,
                'criciuma_identificada': sc_data.get('criciuma', {}).get('casos', 0) > 0,
                'recomendacao': 'Dados disponíveis para análise detalhada' if sc_data.get('total_casos', 0) > 0 else 'Necessário obter mais dados históricos'
            }
        }
        
        cache.set(cache_key, response_data, 3600)
        return Response(response_data)
        
    except Exception as e:
        return Response({
            'error': f'Erro ao buscar dados de SC: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def carregar_estatisticas(request):
    """
    Endpoint para carregar estatísticas do arquivo JSON
    """
    try:
        # Caminho para o arquivo de estatísticas
        stats_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'dengue_statistics.json')
        
        if not os.path.exists(stats_file):
            return Response({
                'error': 'Arquivo dengue_statistics.json não encontrado. Execute o processamento primeiro.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Ler arquivo JSON
        with open(stats_file, 'r', encoding='utf-8') as f:
            stats_data = json.load(f)
        
        # Salvar ou atualizar no banco
        stat, created = DengueStatistic.objects.get_or_create(
            name='dengue_statistics',
            defaults={'data': stats_data}
        )
        
        if not created:
            stat.data = stats_data
            stat.save()
        
        # Limpar cache
        cache.clear()
        
        return Response({
            'message': 'Estatísticas carregadas com sucesso!',
            'total_registros': stats_data.get('geral', {}).get('total_casos', 0),
            'created': created
        })
        
    except Exception as e:
        return Response({
            'error': f'Erro ao carregar estatísticas: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def health_check(request):
    """
    Health check da API
    """
    return Response({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@api_view(['GET'])
def api_info(request):
    """
    Informações sobre a API
    """
    return Response({
        'name': 'Dengue Dashboard API',
        'version': '1.0.0',
        'description': 'API para análise de dados de dengue do DATASUS',
        'endpoints': {
            'dashboard_overview': '/api/dashboard/',
            'estatisticas_por_estado': '/api/estados/',
            'estatisticas_por_ano': '/api/anos/',
            'sintomas_mais_comuns': '/api/sintomas/',
            'santa_catarina_detalhes': '/api/santa-catarina/',
            'carregar_estatisticas': '/api/carregar-estatisticas/',
            'health_check': '/api/health/'
        }
    })