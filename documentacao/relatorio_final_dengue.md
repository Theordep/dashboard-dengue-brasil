# Relatório Final: Análise de Dados de Dengue com Python e Pandas

## 📊 Trabalho de Estatística Aplicada - Engenharia de Software

### 🎯 Objetivo
Demonstrar como a Engenharia de Software, Python e Estatística podem ser aplicados para analisar dados de saúde pública, especificamente casos de dengue, com foco na cidade de Criciúma/SC.

---

## 🔍 Análise Realizada

### 📈 Dados Analisados
- **Dataset**: DENGBR25.csv (DATASUS)
- **Período**: 2025 (dados de janeiro e fevereiro)
- **Amostra**: 50.000 registros
- **Variáveis**: 121 colunas com informações demográficas, clínicas e geográficas

### 🗺️ Distribuição Geográfica
**Top 5 Estados com Mais Casos:**
1. **Goiás (UF 52)**: 26.178 casos (52.4%)
2. **Bahia (UF 29)**: 6.684 casos (13.4%)
3. **Acre (UF 12)**: 4.890 casos (9.8%)
4. **Minas Gerais (UF 31)**: 4.819 casos (9.6%)
5. **Distrito Federal (UF 53)**: 2.818 casos (5.6%)

**Santa Catarina (UF 42)**: 25 casos
- Criciúma não aparece nos dados de 2025 (código 4204608)
- Principais municípios de SC com casos: Florianópolis (12), Joinville (7)

### 👥 Perfil Demográfico

#### Distribuição por Sexo
- **Feminino**: 27.601 casos (55.2%)
- **Masculino**: 22.361 casos (44.7%)
- **Ignorado**: 38 casos (0.1%)

#### Análise Temporal
- **Janeiro 2025**: 20.290 casos
- **Fevereiro 2025**: 29.710 casos
- **Crescimento**: 46.5% entre janeiro e fevereiro

### 🦠 Sintomas Mais Comuns
1. **Febre**: 42.209 casos (84.4%)
2. **Cefaleia**: 39.303 casos (78.6%)
3. **Mialgia**: 38.062 casos (76.1%)
4. **Náusea**: 20.957 casos (41.9%)
5. **Vômito**: 15.280 casos (30.6%)

### 📋 Classificação e Evolução
#### Classificação Final
- **Confirmado**: 39.083 casos (78.2%)
- **Descartado**: 9.514 casos (19.0%)
- **Inconclusivo**: 1.217 casos (2.4%)
- **Óbito por dengue**: 83 casos (0.2%)

#### Evolução dos Casos
- **Cura**: 38.205 casos (76.4%)
- **Ignorado**: 1.055 casos (2.1%)
- **Óbito por dengue**: 39 casos (0.1%)
- **Óbito em investigação**: 14 casos (0.0%)

---

## 🏙️ Análise Específica para Criciúma

### 📊 Situação Atual
- **Casos em 2025**: Não identificados na amostra analisada
- **Dados históricos**: Necessário obter dados de anos anteriores
- **Código IBGE**: 4204608

### 🎯 Próximos Passos para Análise Completa

#### 1. **Obtenção de Dados**
- [ ] Baixar dataset completo do DATASUS (sem limite de linhas)
- [ ] Obter dados históricos (2020-2024)
- [ ] Verificar dados da Secretaria de Saúde de Criciúma

#### 2. **Dados Geográficos**
- [ ] Mapa de bairros de Criciúma
- [ ] Coordenadas geográficas dos casos
- [ ] Setores censitários do IBGE
- [ ] Dados socioeconômicos por bairro

#### 3. **Análises Propostas**
- [ ] **Casos por bairro** com visualização em mapa
- [ ] **Densidade de casos** por área
- [ ] **Análise sazonal** específica da região
- [ ] **Correlação climática** (temperatura, chuva)
- [ ] **Fatores de risco** socioeconômicos
- [ ] **Comparação** com outras cidades de SC

---

## 🛠️ Tecnologias Utilizadas

### 📚 Bibliotecas Python
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica
- **Matplotlib**: Visualizações básicas
- **Seaborn**: Visualizações estatísticas avançadas

### 💻 Scripts Desenvolvidos
1. **analise_dengue_criciuma.py**: Versão inicial
2. **analise_dengue_melhorada.py**: Versão com tratamento de erros
3. **analise_dengue_final.py**: Análise completa e robusta
4. **script_criciuma_especifico.py**: Preparado para análise específica

---

## 📊 Visualizações Geradas

### 🎨 Gráficos Criados
1. **distribuicao_por_uf.png**: Casos por estado
2. **distribuicao_sexo.png**: Distribuição por sexo
3. **distribuicao_idades.png**: Histograma de idades
4. **casos_por_mes.png**: Evolução temporal
5. **sintomas_comuns.png**: Sintomas mais frequentes

---

## 🎓 Contribuições para o Workshop

### 🔬 Engenharia de Software
- **Tratamento de dados**: Limpeza e preparação de datasets grandes
- **Modularização**: Código organizado em funções específicas
- **Tratamento de erros**: Robustez na manipulação de dados
- **Documentação**: Código bem documentado e comentado

### 📈 Estatística Aplicada
- **Análise exploratória**: Descoberta de padrões nos dados
- **Estatísticas descritivas**: Medidas de tendência central e dispersão
- **Análise temporal**: Identificação de tendências e sazonalidade
- **Análise geográfica**: Distribuição espacial dos casos

### 🐍 Python para Ciência de Dados
- **Pandas**: Manipulação eficiente de grandes datasets
- **Visualizações**: Gráficos informativos e profissionais
- **Análise automatizada**: Scripts reutilizáveis e escaláveis

---

## 🌟 Próximas Desenvolvimentos

### 🔮 Funcionalidades Avançadas
- **Mapas interativos** com Folium
- **Machine Learning** para predição de surtos
- **Dashboard web** com Streamlit
- **Análise de séries temporais** avançada
- **Correlação com dados climáticos**

### 📱 Aplicações Práticas
- **Sistema de alerta** para autoridades de saúde
- **Plataforma de monitoramento** em tempo real
- **Relatórios automatizados** para gestores
- **Visualizações interativas** para a população

---

## 📝 Conclusões

Este trabalho demonstra como a **Engenharia de Software** e a **Estatística** podem ser aplicadas de forma integrada para:

1. **Analisar problemas reais** de saúde pública
2. **Processar grandes volumes** de dados eficientemente
3. **Gerar insights** úteis para tomada de decisão
4. **Criar ferramentas** que podem impactar a comunidade
5. **Contribuir** para políticas públicas baseadas em evidências

### 🎯 Impacto Social
- **Prevenção**: Identificação de áreas de risco
- **Planejamento**: Alocação eficiente de recursos
- **Educação**: Conscientização da população
- **Pesquisa**: Base para estudos epidemiológicos

---

## 📚 Referências
- **DATASUS**: Departamento de Informática do SUS
- **IBGE**: Instituto Brasileiro de Geografia e Estatística
- **Ministério da Saúde**: Dados epidemiológicos
- **Python Data Science Handbook**: Jake VanderPlas
- **Pandas Documentation**: pandas.pydata.org

---

*Trabalho desenvolvido para a disciplina de Estatística Aplicada - Engenharia de Software*
