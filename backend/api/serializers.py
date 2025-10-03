from rest_framework import serializers
from .models import DengueStatistic, Estado, Municipio, CasoDengue, DashboardCache

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['codigo_uf', 'nome', 'total_casos']

class MunicipioSerializer(serializers.ModelSerializer):
    estado_nome = serializers.CharField(source='estado.nome', read_only=True)
    
    class Meta:
        model = Municipio
        fields = ['codigo_ibge', 'nome', 'estado_nome', 'total_casos']

class CasoDengueSerializer(serializers.ModelSerializer):
    estado_nome = serializers.CharField(source='estado.nome', read_only=True)
    municipio_nome = serializers.CharField(source='municipio.nome', read_only=True)
    
    class Meta:
        model = CasoDengue
        fields = [
            'id', 'data_notificacao', 'ano', 'mes',
            'estado_nome', 'municipio_nome', 'sexo', 'idade',
            'febre', 'mialgia', 'cefaleia', 'exantema', 'vomito', 'nausea',
            'classificacao_final', 'evolucao', 'created_at'
        ]

class DengueStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = DengueStatistic
        fields = ['name', 'data', 'created_at', 'updated_at']

class DashboardCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardCache
        fields = ['cache_key', 'data', 'expires_at', 'created_at']

# Serializers para dados agregados
class EstatisticasGeraisSerializer(serializers.Serializer):
    total_casos = serializers.IntegerField()
    periodo_inicio = serializers.CharField()
    periodo_fim = serializers.CharField()
    anos_disponiveis = serializers.ListField(child=serializers.IntegerField())
    estados_unicos = serializers.IntegerField()

class PorEstadoSerializer(serializers.Serializer):
    uf = serializers.ListField(child=serializers.CharField())
    casos = serializers.ListField(child=serializers.IntegerField())
    percentual = serializers.ListField(child=serializers.FloatField(), required=False)

class PorAnoSerializer(serializers.Serializer):
    anos = serializers.ListField(child=serializers.IntegerField())
    casos = serializers.ListField(child=serializers.IntegerField())

class DemograficoSerializer(serializers.Serializer):
    sexo = serializers.DictField()
    idade = serializers.DictField(required=False)

class SintomasSerializer(serializers.Serializer):
    sintoma = serializers.CharField()
    casos = serializers.IntegerField()
    percentual = serializers.FloatField()

class SantaCatarinaSerializer(serializers.Serializer):
    total_casos = serializers.IntegerField()
    municipios_afetados = serializers.IntegerField()
    municipios = serializers.DictField(required=False)
    criciuma = serializers.DictField(required=False)
