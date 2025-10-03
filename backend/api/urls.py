from django.urls import path
from . import views
from . import views_advanced

urlpatterns = [
    # Endpoints principais
    path('', views.dashboard_overview, name='dashboard_overview'),
    path('dashboard/', views.dashboard_overview, name='dashboard_overview'),
    
    # Estatísticas específicas
    path('estados/', views.estatisticas_por_estado, name='estatisticas_por_estado'),
    path('anos/', views.estatisticas_por_ano, name='estatisticas_por_ano'),
    path('sintomas/', views.sintomas_mais_comuns, name='sintomas_mais_comuns'),
    path('santa-catarina/', views.santa_catarina_detalhes, name='santa_catarina_detalhes'),
    
    # Gerenciamento
    path('carregar-estatisticas/', views.carregar_estatisticas, name='carregar_estatisticas'),
    
    # Utilitários
    path('health/', views.health_check, name='health_check'),
    path('info/', views.api_info, name='api_info'),
    
    # Endpoints avançados
    path('avancado/faixas-etarias/', views_advanced.faixas_etarias, name='faixas_etarias'),
    path('avancado/genero/', views_advanced.genero_detalhado, name='genero_detalhado'),
    path('avancado/santa-catarina/', views_advanced.santa_catarina_avancado, name='santa_catarina_avancado'),
    path('avancado/sintomas-por-perfil/', views_advanced.sintomas_por_perfil, name='sintomas_por_perfil'),
    path('avancado/carregar-estatisticas/', views_advanced.carregar_estatisticas_avancadas, name='carregar_estatisticas_avancadas'),
]