from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json

class DengueStatistic(models.Model):
    """
    Modelo para armazenar estatísticas gerais de dengue
    """
    name = models.CharField(max_length=100, unique=True)
    data = models.JSONField(encoder=DjangoJSONEncoder)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Estatística de Dengue"
        verbose_name_plural = "Estatísticas de Dengue"

class Estado(models.Model):
    """
    Modelo para armazenar dados por estado
    """
    codigo_uf = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=100)
    total_casos = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.nome} ({self.codigo_uf})"
    
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

class Municipio(models.Model):
    """
    Modelo para armazenar dados por município
    """
    codigo_ibge = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=200)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    total_casos = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.nome} - {self.estado.nome}"
    
    class Meta:
        verbose_name = "Município"
        verbose_name_plural = "Municípios"

class CasoDengue(models.Model):
    """
    Modelo para armazenar casos individuais de dengue
    """
    SEXO_CHOICES = [
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('I', 'Ignorado'),
    ]
    
    CLASSIFICACAO_CHOICES = [
        (10, 'Confirmado'),
        (8, 'Descartado'),
        (11, 'Inconclusivo'),
        (12, 'Óbito por dengue'),
    ]
    
    EVOLUCAO_CHOICES = [
        (1, 'Cura'),
        (2, 'Óbito por dengue'),
        (3, 'Óbito por outras causas'),
        (4, 'Óbito em investigação'),
        (9, 'Ignorado'),
    ]
    
    # Dados básicos
    data_notificacao = models.DateField()
    ano = models.IntegerField()
    mes = models.IntegerField()
    
    # Localização
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
    
    # Demográficos
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    idade = models.IntegerField(null=True, blank=True)
    
    # Clínicos
    febre = models.BooleanField(default=False)
    mialgia = models.BooleanField(default=False)
    cefaleia = models.BooleanField(default=False)
    exantema = models.BooleanField(default=False)
    vomito = models.BooleanField(default=False)
    nausea = models.BooleanField(default=False)
    
    # Classificação
    classificacao_final = models.IntegerField(choices=CLASSIFICACAO_CHOICES, null=True, blank=True)
    evolucao = models.IntegerField(choices=EVOLUCAO_CHOICES, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Caso {self.id} - {self.estado.nome} - {self.data_notificacao}"
    
    class Meta:
        verbose_name = "Caso de Dengue"
        verbose_name_plural = "Casos de Dengue"
        ordering = ['-data_notificacao']

class DashboardCache(models.Model):
    """
    Modelo para cache de dados do dashboard
    """
    cache_key = models.CharField(max_length=100, unique=True)
    data = models.JSONField(encoder=DjangoJSONEncoder)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cache_key
    
    class Meta:
        verbose_name = "Cache do Dashboard"
        verbose_name_plural = "Caches do Dashboard"