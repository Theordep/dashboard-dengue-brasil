# 🦟 Dashboard de Dengue - Sistema Completo

## 📊 Projeto Full-Stack: Django + React + SQLite

### 🎯 Objetivo
Sistema completo para análise e visualização de dados de dengue do DATASUS, com foco especial em **Criciúma/SC** e análise por bairros.

---

## 🏗️ Arquitetura do Sistema

```
ProjetoPythonDengue/
├── 📊 Dados
│   ├── DENGBR25.csv (397MB - 1.5M registros)
│   └── dengue_statistics.json (estatísticas processadas)
├── 🐍 Backend (Django API)
│   ├── Models para dengue
│   ├── API REST endpoints
│   └── Banco SQLite
├── ⚛️ Frontend (React)
│   ├── Dashboard interativo
│   ├── Gráficos com Recharts
│   └── Material-UI
└── 📈 Scripts de Processamento
    ├── Processamento de dados
    └── Testes de integração
```

---

## 🚀 Como Executar o Sistema

### 1️⃣ **Pré-requisitos**
```bash
# Python 3.11+
pip install django djangorestframework django-cors-headers pandas numpy matplotlib seaborn

# Node.js 16+
npm install axios recharts react-router-dom @mui/material @emotion/react @emotion/styled @mui/icons-material
```

### 2️⃣ **Processamento dos Dados**
```bash
# No diretório raiz
python data_processor_simple.py
```
- Processa o arquivo CSV completo (1.5M registros)
- Gera estatísticas em JSON
- Tempo estimado: 2-3 minutos

### 3️⃣ **Backend Django**
```bash
cd backend

# Configurar banco
python manage.py makemigrations
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```
- API disponível em: `http://localhost:8000`
- Admin Django: `http://localhost:8000/admin`

### 4️⃣ **Frontend React**
```bash
cd frontend

# Instalar dependências
npm install

# Iniciar aplicação
npm start
```
- Dashboard disponível em: `http://localhost:3000`

### 5️⃣ **Teste de Integração**
```bash
# No diretório raiz
python test_integration.py
```

---

## 📊 Dados Processados

### 🔢 **Estatísticas Gerais**
- **Total de registros**: 1.502.259 casos
- **Período**: 2024-2025
- **Estados**: 27 estados brasileiros
- **Santa Catarina**: 27.082 casos

### 🏙️ **Santa Catarina Específico**
- **Total de casos**: 27.082
- **Municípios afetados**: Múltiplos
- **Criciúma**: 0 casos identificados (necessário dados históricos)

### 🦠 **Sintomas Mais Comuns**
1. **Febre**: 84.4% dos casos
2. **Cefaleia**: 78.6% dos casos
3. **Mialgia**: 76.1% dos casos

---

## 🛠️ Funcionalidades Implementadas

### 🔧 **Backend (Django)**
- ✅ **Models**: DengueStatistic, Estado, Municipio, CasoDengue
- ✅ **API REST**: Endpoints para todas as estatísticas
- ✅ **Cache**: Sistema de cache para performance
- ✅ **Admin**: Interface administrativa completa
- ✅ **CORS**: Configurado para React

### 🎨 **Frontend (React)**
- ✅ **Dashboard**: Visão geral com estatísticas principais
- ✅ **Gráficos**: Estados, sintomas, anos (Recharts)
- ✅ **Material-UI**: Interface moderna e responsiva
- ✅ **Santa Catarina**: Seção específica com análise de Criciúma
- ✅ **Responsivo**: Funciona em desktop e mobile

### 📈 **Visualizações**
- ✅ **Gráfico de Barras**: Casos por estado
- ✅ **Gráfico de Linha**: Evolução por ano
- ✅ **Gráfico Horizontal**: Sintomas mais comuns
- ✅ **Cards**: Estatísticas gerais
- ✅ **Alertas**: Status e recomendações

---

## 🎯 Endpoints da API

### 📡 **Principais**
- `GET /api/dashboard/` - Visão geral completa
- `GET /api/estados/` - Estatísticas por estado
- `GET /api/sintomas/` - Sintomas mais comuns
- `GET /api/santa-catarina/` - Dados específicos de SC

### 🔧 **Utilitários**
- `POST /api/carregar-estatisticas/` - Carregar dados do JSON
- `GET /api/health/` - Health check
- `GET /api/info/` - Informações da API

---

## 🏙️ Análise de Criciúma

### 📊 **Status Atual**
- **Código IBGE**: 4204608
- **Casos identificados**: 0 (dados 2024-2025)
- **Necessário**: Dados históricos e geográficos

### 🎯 **Próximos Passos**
1. **Obter dados históricos** (2020-2023)
2. **Dados geográficos** (mapas de bairros)
3. **Coordenadas GPS** dos casos
4. **Análise por setor censitário** (IBGE)
5. **Correlação climática** (INMET)

### 💡 **Estratégias Propostas**
```python
# Exemplo de análise por bairro
import geopandas as gpd
from shapely.geometry import Point

def analisar_por_bairro(casos_df, bairros_gdf):
    # 1. Criar pontos geográficos dos casos
    geometria_casos = [Point(xy) for xy in zip(casos_df['LONGITUDE'], 
                                              casos_df['LATITUDE'])]
    casos_gdf = gpd.GeoDataFrame(casos_df, geometry=geometria_casos)
    
    # 2. Fazer join espacial com bairros
    casos_por_bairro = gpd.sjoin(casos_gdf, bairros_gdf, how='left')
    
    # 3. Contar casos por bairro
    contagem_bairros = casos_por_bairro.groupby('NOME_BAIRRO').size()
    
    return contagem_bairros
```

---

## 🔮 Evoluções Futuras

### 📱 **Funcionalidades Avançadas**
- [ ] **Mapas interativos** com Folium/Leaflet
- [ ] **Machine Learning** para predição de surtos
- [ ] **Dashboard em tempo real** com WebSockets
- [ ] **App mobile** para reporte de focos
- [ ] **Análise de séries temporais** avançada

### 🛠️ **Melhorias Técnicas**
- [ ] **Docker** para containerização
- [ ] **PostgreSQL** para dados maiores
- [ ] **Redis** para cache distribuído
- [ ] **Deploy** em cloud (AWS/Azure)
- [ ] **CI/CD** com GitHub Actions

---

## 📚 Tecnologias Utilizadas

### 🐍 **Backend**
- **Django 5.2.7**: Framework web
- **Django REST Framework**: API REST
- **SQLite**: Banco de dados local
- **Pandas**: Processamento de dados
- **NumPy**: Computação numérica

### ⚛️ **Frontend**
- **React 18**: Biblioteca de interface
- **Material-UI**: Componentes de interface
- **Recharts**: Gráficos e visualizações
- **Axios**: Cliente HTTP
- **React Router**: Navegação

### 📊 **Visualização**
- **Matplotlib**: Gráficos estáticos
- **Seaborn**: Visualizações estatísticas
- **Recharts**: Gráficos interativos
- **Material-UI**: Interface moderna

---

## 🎓 Contribuições Acadêmicas

### 🔬 **Engenharia de Software**
- **Arquitetura full-stack** moderna
- **API REST** bem estruturada
- **Código modular** e reutilizável
- **Documentação completa**
- **Testes de integração**

### 📈 **Estatística Aplicada**
- **Análise exploratória** de grandes datasets
- **Visualizações estatísticas** profissionais
- **Processamento de 1.5M registros**
- **Análise demográfica** e epidemiológica
- **Correlações temporais** e geográficas

### 🐍 **Python para Ciência de Dados**
- **Pandas** para manipulação eficiente
- **Processamento em lote** de grandes volumes
- **Análise estatística** automatizada
- **Visualizações** programáticas
- **Integração** com APIs web

---

## 🌟 Impacto Social

### 🏥 **Saúde Pública**
- **Identificação precoce** de surtos
- **Monitoramento** em tempo real
- **Dados para políticas** públicas
- **Base para pesquisas** epidemiológicas

### 💼 **Gestão de Recursos**
- **Alocação eficiente** de inseticidas
- **Priorização** de áreas de risco
- **Otimização** de campanhas preventivas
- **Redução de custos** operacionais

### 👥 **Educação e Conscientização**
- **Dashboard público** para população
- **Dados transparentes** e acessíveis
- **Visualizações** educativas
- **Engajamento** comunitário

---

## 📞 Suporte e Contato

### 🐛 **Problemas Conhecidos**
- **Encoding**: Emojis removidos para compatibilidade Windows
- **Performance**: Cache implementado para otimização
- **CORS**: Configurado para desenvolvimento local

### 📖 **Documentação**
- **Código comentado** em português
- **README** detalhado
- **Endpoints** documentados
- **Exemplos** de uso

### 🔄 **Atualizações**
- **Versão atual**: 1.0.0
- **Última atualização**: Janeiro 2025
- **Compatibilidade**: Python 3.11+, Node.js 16+

---

## 🙏 Agradecimentos

- **DATASUS** pela disponibilização dos dados
- **Django** e **React** pelas tecnologias
- **Material-UI** pelos componentes
- **Comunidade Python** pelo suporte
- **Professores** de Estatística Aplicada

---

*Desenvolvido para demonstração de como Engenharia de Software + Estatística + Python podem impactar a saúde pública brasileira* 🇧🇷
