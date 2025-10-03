# Fluxo Completo do Sistema de Análise de Dengue

Este documento explica detalhadamente o fluxo completo do sistema, desde o processamento inicial dos dados brutos até a visualização no dashboard.

## 1. Dados Brutos: DENGBR25.csv

### 1.1 Origem e Estrutura

O arquivo `DENGBR25.csv` é a fonte primária de dados do sistema, contendo registros de casos de dengue do DATASUS. Este arquivo contém mais de 1,5 milhão de registros com mais de 100 colunas, incluindo:

- Dados de notificação (data, local)
- Informações demográficas (idade, sexo)
- Sintomas (febre, mialgia, cefaleia, etc.)
- Evolução clínica (cura, óbito)
- Classificação final dos casos

### 1.2 Localização e Acesso

O arquivo está armazenado em `Documentos/DENGBR25.csv` e é acessado pelos processadores de dados. Devido ao seu grande tamanho, o arquivo não é versionado no repositório.

## 2. Processamento de Dados

### 2.1 Processador Principal (data_processor.py)

O arquivo `data_processor.py` é responsável pela transformação dos dados brutos em informações estruturadas. Este processador:

1. **Carrega o CSV**: Utiliza pandas para carregar o arquivo CSV em um DataFrame
   ```python
   self.df = pd.read_csv(self.csv_path, low_memory=False)
   ```

2. **Converte tipos de dados**: Transforma strings em datas, números, etc.
   ```python
   self.df['DT_NOTIFIC'] = pd.to_datetime(self.df['DT_NOTIFIC'], errors='coerce')
   self.df['NU_IDADE_N'] = pd.to_numeric(self.df['NU_IDADE_N'], errors='coerce')
   ```

3. **Gera estatísticas gerais**:
   - Total de casos
   - Período de tempo coberto
   - Anos disponíveis
   - Estados afetados

4. **Calcula estatísticas por estado**:
   ```python
   casos_por_uf = self.df['SG_UF_NOT'].value_counts().head(20)
   self.stats['por_estado'] = {
       'uf': casos_por_uf.index.tolist(),
       'casos': casos_por_uf.values.tolist()
   }
   ```

5. **Calcula estatísticas por ano**:
   ```python
   casos_por_ano = self.df['NU_ANO'].value_counts().sort_index()
   self.stats['por_ano'] = {
       'anos': casos_por_ano.index.tolist(),
       'casos': casos_por_ano.values.tolist()
   }
   ```

6. **Analisa dados demográficos**:
   - Distribuição por sexo
   - Sintomas mais comuns

7. **Foco em Santa Catarina**:
   - Filtra dados específicos de SC
   - Identifica municípios mais afetados
   - Destaca Criciúma

8. **Salva resultados em JSON**:
   ```python
   with open(output_file, 'w', encoding='utf-8') as f:
       json.dump(self.stats, f, ensure_ascii=False, indent=2)
   ```

### 2.2 Processador Avançado (data_processor_advanced.py)

O processador avançado estende o processador básico com análises mais sofisticadas:

1. **Conversão de idade**: Transforma o código de idade em idade real em anos
   ```python
   def _convert_age(self):
       # Valores < 1000 são idades em anos
       mask_anos = self.df['NU_IDADE_N'] < 1000
       self.df.loc[mask_anos, 'IDADE_ANOS'] = self.df.loc[mask_anos, 'NU_IDADE_N']
       
       # Valores >= 1000 são codificados
       # Primeira posição (milhar): 1=dia, 2=mês, 3=ano
       mask_codificados = self.df['NU_IDADE_N'] >= 1000
       unidade = (self.df.loc[mask_codificados, 'NU_IDADE_N'] // 1000).astype(int)
       valor = self.df.loc[mask_codificados, 'NU_IDADE_N'] % 1000
       
       # Converter para anos
       mask_dias = mask_codificados & (unidade == 1)
       self.df.loc[mask_dias, 'IDADE_ANOS'] = valor[mask_dias] / 365
       
       mask_meses = mask_codificados & (unidade == 2)
       self.df.loc[mask_meses, 'IDADE_ANOS'] = valor[mask_meses] / 12
       
       mask_anos_cod = mask_codificados & (unidade == 3)
       self.df.loc[mask_anos_cod, 'IDADE_ANOS'] = valor[mask_anos_cod]
   ```

2. **Categorização por faixa etária**:
   ```python
   def _categorize_age_groups(self):
       bins = [0, 5, 15, 30, 45, 60, 150]
       labels = ['0-4', '5-14', '15-29', '30-44', '45-59', '60+']
       
       self.df['FAIXA_ETARIA'] = pd.cut(
           self.df['IDADE_ANOS'], 
           bins=bins, 
           labels=labels, 
           right=False
       )
   ```

3. **Análise detalhada por faixa etária**:
   - Contagem de casos por faixa
   - Óbitos por faixa
   - Taxa de letalidade por faixa

4. **Análise detalhada por gênero**:
   - Distribuição por faixa etária e gênero
   - Sintomas mais comuns por gênero
   - Evolução clínica por gênero

5. **Análise detalhada de Santa Catarina**:
   - Top 10 municípios
   - Análise temporal (mês a mês)
   - Comparação com média nacional
   - Taxa de incidência por 100 mil habitantes

6. **Análise de sintomas por perfil**:
   - Sintomas por faixa etária
   - Combinações de sintomas mais frequentes

7. **Salva estatísticas avançadas em JSON**:
   ```python
   with open('dengue_advanced_statistics.json', 'w', encoding='utf-8') as f:
       json.dump(self.stats, f, ensure_ascii=False, indent=2)
   ```

### 2.3 Cálculos Estatísticos

O sistema realiza diversos cálculos estatísticos:

1. **Contagens e percentuais**:
   ```python
   total_casos = len(casos_faixa)
   percentual = (total_casos / len(self.df)) * 100
   ```

2. **Taxas de letalidade**:
   ```python
   obitos = len(casos_faixa[casos_faixa['EVOLUCAO'] == 2])
   taxa_letalidade = (obitos / total_casos * 100) if total_casos > 0 else 0
   ```

3. **Taxas de incidência**:
   ```python
   incidencia_sc = (casos_sc / pop_sc) * 100000
   incidencia_br = (total_nacional / pop_br) * 100000
   ```

4. **Crescimento percentual**:
   ```python
   crescimento = ((mes_atual - mes_anterior) / mes_anterior) * 100
   ```

5. **Correlações e agrupamentos**:
   - Agrupamento por UF, município, faixa etária
   - Correlação entre sintomas
   - Análise temporal de tendências

## 3. Armazenamento de Dados Processados

### 3.1 Arquivos JSON

Os dados processados são armazenados em arquivos JSON:

1. **dengue_statistics.json**: Estatísticas básicas
   ```json
   {
     "geral": {
       "total_casos": 1502259,
       "periodo_inicio": "2024-12-29 00:00:00",
       "periodo_fim": "2025-07-05 00:00:00",
       "anos_disponiveis": [2024, 2025],
       "estados_unicos": 27
     },
     "por_estado": { ... },
     "por_ano": { ... },
     "demografico": { ... },
     "sintomas": { ... },
     "santa_catarina": { ... }
   }
   ```

2. **dengue_advanced_statistics.json**: Estatísticas avançadas
   ```json
   {
     "geral": { ... },
     "por_estado": { ... },
     "por_ano": { ... },
     "demografico": { ... },
     "sintomas": { ... },
     "faixa_etaria": {
       "0-4": { "casos": 5728, "obitos": 8, "letalidade": 0.139, ... },
       "5-14": { "casos": 6305, "obitos": 7, "letalidade": 0.111, ... },
       ...
     },
     "genero_detalhado": { ... },
     "santa_catarina": { ... },
     "sintomas_por_perfil": { ... }
   }
   ```

## 4. Backend (Django)

### 4.1 Estrutura do Backend

O backend é construído com Django e Django REST Framework, organizado em:

- **models.py**: Define os modelos de dados
- **views.py**: Implementa os endpoints da API
- **views_advanced.py**: Implementa endpoints para estatísticas avançadas
- **urls.py**: Define as rotas da API

### 4.2 Modelos de Dados

O backend utiliza os seguintes modelos para armazenar os dados:

1. **DengueStatistic**: Armazena estatísticas gerais como JSON
   ```python
   class DengueStatistic(models.Model):
       name = models.CharField(max_length=100, unique=True)
       data = models.JSONField(encoder=DjangoJSONEncoder)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
   ```

2. **Estado**: Armazena informações de estados
   ```python
   class Estado(models.Model):
       codigo_uf = models.CharField(max_length=2, unique=True)
       nome = models.CharField(max_length=100)
       total_casos = models.IntegerField(default=0)
   ```

3. **Municipio**: Armazena informações de municípios
   ```python
   class Municipio(models.Model):
       codigo_ibge = models.CharField(max_length=10, unique=True)
       nome = models.CharField(max_length=200)
       estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
       total_casos = models.IntegerField(default=0)
   ```

4. **CasoDengue**: Armazena casos individuais
   ```python
   class CasoDengue(models.Model):
       data_notificacao = models.DateField()
       ano = models.IntegerField()
       mes = models.IntegerField()
       estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
       municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True)
       sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
       idade = models.IntegerField(null=True, blank=True)
       febre = models.BooleanField(default=False)
       # ... outros sintomas e informações clínicas
   ```

5. **DashboardCache**: Armazena cache de dados para o dashboard
   ```python
   class DashboardCache(models.Model):
       cache_key = models.CharField(max_length=100, unique=True)
       data = models.JSONField(encoder=DjangoJSONEncoder)
       expires_at = models.DateTimeField()
   ```

### 4.3 Carregamento de Dados

O backend carrega os dados dos arquivos JSON para o banco de dados:

```python
@api_view(['POST'])
def carregar_estatisticas(request):
    try:
        json_file = 'dengue_statistics.json'
        
        if not os.path.exists(json_file):
            return Response({
                'error': f'Arquivo {json_file} não encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Salvar no banco de dados
        stat, created = DengueStatistic.objects.update_or_create(
            name='dengue_statistics',
            defaults={'data': data}
        )
        
        # Limpar cache
        cache.delete_many(['dashboard_overview', 'estatisticas_por_estado', 
                          'estatisticas_por_ano', 'sintomas_mais_comuns',
                          'santa_catarina_detalhes'])
        
        return Response({
            'message': 'Estatísticas carregadas com sucesso!',
            'created': created
        })
        
    except Exception as e:
        return Response({
            'error': f'Erro ao carregar estatísticas: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

De forma similar, as estatísticas avançadas são carregadas pelo endpoint `carregar_estatisticas_avancadas`.

### 4.4 Endpoints da API

O backend expõe os seguintes endpoints:

1. **Endpoints Básicos**:
   - `/api/dashboard/`: Visão geral do dashboard
   - `/api/estados/`: Estatísticas por estado
   - `/api/anos/`: Estatísticas por ano
   - `/api/sintomas/`: Sintomas mais comuns
   - `/api/santa-catarina/`: Detalhes de Santa Catarina

2. **Endpoints Avançados**:
   - `/api/avancado/faixas-etarias/`: Estatísticas por faixa etária
   - `/api/avancado/genero/`: Análise detalhada por gênero
   - `/api/avancado/santa-catarina/`: Análise avançada de SC
   - `/api/avancado/sintomas-por-perfil/`: Sintomas por perfil

3. **Endpoints de Gerenciamento**:
   - `/api/carregar-estatisticas/`: Carrega estatísticas básicas
   - `/api/avancado/carregar-estatisticas/`: Carrega estatísticas avançadas
   - `/api/health/`: Verificação de saúde da API
   - `/api/info/`: Informações sobre a API

### 4.5 Cache

O backend utiliza o sistema de cache do Django para melhorar a performance:

```python
cache_key = 'dashboard_overview'
cached_data = cache.get(cache_key)

if cached_data:
    return Response(cached_data)

# ... processar dados ...

cache.set(cache_key, response_data, 3600)  # Cache por 1 hora
```

## 5. Frontend (Next.js)

### 5.1 Estrutura do Frontend

O frontend é construído com Next.js e Tailwind CSS, organizado em:

- **app/**: Páginas da aplicação
- **components/**: Componentes reutilizáveis
- **services/**: Serviços para comunicação com a API

### 5.2 Serviço de API

O frontend se comunica com o backend através de um serviço de API:

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

export const apiService = {
  getDashboardData: () => {
    return api.get('/dashboard/');
  },
  getEstadosData: () => {
    return api.get('/estados/');
  },
  // ... outros métodos ...
};
```

### 5.3 Carregamento de Dados

As páginas carregam dados da API usando hooks do React:

```javascript
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  const loadData = async () => {
    try {
      setLoading(true);
      const response = await apiService.getDashboardData();
      setData(response.data);
    } catch (err) {
      setError('Erro ao carregar dados');
    } finally {
      setLoading(false);
    }
  };

  loadData();
}, []);
```

### 5.4 Visualização de Dados

O frontend utiliza diversos componentes de visualização:

1. **Gráficos**:
   - `GraficoEstados`: Barra para casos por estado
   - `GraficoAnos`: Linha para evolução temporal
   - `GraficoSintomas`: Barra para sintomas comuns
   - `GraficoFaixaEtaria`: Barra para faixas etárias
   - `GraficoGenero`: Barra para distribuição por gênero
   - `GraficoSintomasPerfil`: Radar para sintomas por perfil
   - `GraficoSCAvancado`: Componentes para análise de SC

2. **Componentes de Dashboard**:
   - `EstatisticasGerais`: Cards com estatísticas principais
   - `SantaCatarina`: Análise detalhada de SC
   - `ApiStatus`: Status de conexão com a API

### 5.5 Páginas

O frontend possui as seguintes páginas:

1. **Dashboard Principal** (`/`):
   - Estatísticas gerais
   - Distribuição nacional de casos
   - Sintomas mais comuns
   - Evolução temporal

2. **Santa Catarina** (`/santa-catarina`):
   - Análise detalhada do estado
   - Municípios mais afetados
   - Detalhes por município

3. **Análise Avançada** (`/analise-avancada`):
   - Análise por faixa etária
   - Análise por gênero
   - Análise clínica
   - Análise detalhada de SC

4. **Sobre** (`/sobre`):
   - Informações sobre o projeto
   - Metodologia
   - Fontes de dados

## 6. Fluxo Completo de Dados

### 6.1 Visão Geral

O fluxo completo de dados no sistema segue estas etapas:

1. **Entrada**: Arquivo CSV com dados brutos do DATASUS
2. **Processamento**: Scripts Python transformam os dados em estatísticas
3. **Armazenamento Intermediário**: Estatísticas salvas em arquivos JSON
4. **Backend**: API Django carrega os dados JSON para o banco de dados
5. **API**: Endpoints REST expõem os dados processados
6. **Frontend**: Interface web consome a API e exibe visualizações
7. **Usuário Final**: Visualiza e interage com os dados através do dashboard

### 6.2 Diagrama de Fluxo

```
┌───────────┐     ┌───────────────┐     ┌──────────┐     ┌─────────┐     ┌──────────┐
│           │     │               │     │          │     │         │     │          │
│ DENGBR25  │────▶│ Processadores │────▶│  JSON    │────▶│ Backend │────▶│ Frontend │
│   .csv    │     │    Python     │     │ Arquivos │     │ Django  │     │ Next.js  │
│           │     │               │     │          │     │         │     │          │
└───────────┘     └───────────────┘     └──────────┘     └─────────┘     └──────────┘
```

## 7. Conceitos Estatísticos Aplicados

### 7.1 Medidas de Tendência Central

- **Contagem**: Total de casos, casos por estado, etc.
- **Percentuais**: Proporção de casos por categoria
- **Médias**: Média de casos por período

### 7.2 Análise Temporal

- **Séries Temporais**: Evolução de casos ao longo dos anos
- **Crescimento Percentual**: Variação mês a mês
- **Sazonalidade**: Padrões temporais de incidência

### 7.3 Análise Demográfica

- **Estratificação por Idade**: Divisão em faixas etárias
- **Análise por Gênero**: Comparação entre casos masculinos e femininos
- **Taxa de Letalidade**: Proporção de óbitos em relação ao total de casos

### 7.4 Análise Geográfica

- **Distribuição Espacial**: Casos por estado e município
- **Incidência Relativa**: Casos por 100 mil habitantes
- **Comparações Regionais**: Análise específica de Santa Catarina

## 8. Conclusão

Este sistema representa um fluxo completo de processamento, análise e visualização de dados epidemiológicos, transformando dados brutos em informações acionáveis através de:

1. **Processamento eficiente** de grandes volumes de dados
2. **Cálculos estatísticos** para extrair insights relevantes
3. **API robusta** com cache para entrega rápida de dados
4. **Interface intuitiva** para visualização e exploração de dados

O sistema permite uma compreensão aprofundada da situação epidemiológica da dengue no Brasil, com foco especial em Santa Catarina, fornecendo informações valiosas para tomada de decisões em saúde pública.
