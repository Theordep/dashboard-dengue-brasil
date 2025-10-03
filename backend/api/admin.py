from django.contrib import admin
from .models import DengueStatistic, Estado, Municipio, CasoDengue, DashboardCache

@admin.register(DengueStatistic)
class DengueStatisticAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name']

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo_uf', 'total_casos']
    search_fields = ['nome', 'codigo_uf']
    ordering = ['-total_casos']

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'estado', 'total_casos']
    list_filter = ['estado']
    search_fields = ['nome', 'codigo_ibge']
    ordering = ['-total_casos']

@admin.register(CasoDengue)
class CasoDengueAdmin(admin.ModelAdmin):
    list_display = ['id', 'data_notificacao', 'estado', 'municipio', 'sexo', 'classificacao_final']
    list_filter = ['estado', 'sexo', 'classificacao_final', 'evolucao', 'ano']
    search_fields = ['estado__nome', 'municipio__nome']
    date_hierarchy = 'data_notificacao'
    ordering = ['-data_notificacao']

@admin.register(DashboardCache)
class DashboardCacheAdmin(admin.ModelAdmin):
    list_display = ['cache_key', 'expires_at', 'created_at']
    readonly_fields = ['created_at']
    search_fields = ['cache_key']