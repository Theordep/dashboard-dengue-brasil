# 🚀 Como Usar o Sistema de Dashboard de Dengue

## 📋 Passo a Passo Completo

### 1️⃣ **Preparação do Ambiente**

```bash
# Instalar dependências Python
pip install django djangorestframework django-cors-headers pandas numpy matplotlib seaborn requests

# Instalar dependências Node.js (no diretório frontend)
npm install axios recharts react-router-dom @mui/material @emotion/react @emotion/styled @mui/icons-material
```

### 2️⃣ **Processar os Dados**

```bash
# No diretório raiz do projeto
python data_processor_simple.py
```

**O que acontece:**
- Carrega o arquivo DENGBR25.csv completo (1.5M registros)
- Processa e analisa todos os dados
- Gera arquivo `dengue_statistics.json` com estatísticas
- Tempo estimado: 2-3 minutos

### 3️⃣ **Iniciar o Backend Django**

```bash
# Abrir terminal 1
cd backend

# Configurar banco de dados
python manage.py makemigrations
python manage.py migrate

# Iniciar servidor Django
python manage.py runserver
```

**Resultado esperado:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 5.2.7, using settings 'denguedashboard.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 4️⃣ **Iniciar o Frontend React**

```bash
# Abrir terminal 2
cd frontend

# Iniciar aplicação React
npm start
```

**Resultado esperado:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.xxx:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

### 5️⃣ **Carregar Dados na API**

```bash
# Abrir terminal 3 (ou usar Postman/Insomnia)
curl -X POST http://localhost:8000/api/carregar-estatisticas/

# Ou acessar diretamente no navegador:
# http://localhost:8000/api/carregar-estatisticas/
```

### 6️⃣ **Acessar o Dashboard**

**Abrir no navegador:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/

---

## 🎯 Funcionalidades do Dashboard

### 📊 **Página Principal**
- **Estatísticas Gerais**: Total de casos, estados afetados, período
- **Gráfico por Estados**: Top 10 estados com mais casos
- **Gráfico por Anos**: Evolução temporal
- **Sintomas Mais Comuns**: Ranking de sintomas
- **Santa Catarina**: Análise específica com foco em Criciúma

### 🔄 **Botões de Ação**
- **Atualizar Dados**: Recarrega informações da API
- **Responsivo**: Funciona em desktop e mobile

---

## 🏙️ Análise de Criciúma

### 📊 **O que você verá:**
- **Total de casos em SC**: 27.082 casos
- **Criciúma**: 0 casos identificados (dados 2024-2025)
- **Recomendações**: Próximos passos para análise por bairros

### 🎯 **Por que 0 casos em Criciúma?**
1. **Dados recentes**: Arquivo contém dados de 2024-2025
2. **Necessário**: Dados históricos de anos anteriores
3. **Solução**: Obter dados de 2020-2023 do DATASUS

---

## 🛠️ Solução de Problemas

### ❌ **Erro: "Dados não encontrados"**
```bash
# Solução: Carregar estatísticas na API
curl -X POST http://localhost:8000/api/carregar-estatisticas/
```

### ❌ **Erro: "Connection refused"**
```bash
# Verificar se o Django está rodando
# Terminal: cd backend && python manage.py runserver
```

### ❌ **Erro: "Module not found"**
```bash
# Instalar dependências Python
pip install django djangorestframework django-cors-headers pandas numpy

# Instalar dependências Node.js
cd frontend && npm install
```

### ❌ **Erro: "CORS"**
```bash
# Verificar se django-cors-headers está instalado
pip install django-cors-headers

# Verificar configuração em backend/denguedashboard/settings.py
```

---

## 📈 Dados Disponíveis

### 🔢 **Estatísticas Processadas**
- **1.502.259 casos** de dengue no Brasil
- **27 estados** brasileiros
- **Período**: 2024-2025
- **Santa Catarina**: 27.082 casos

### 📊 **Visualizações**
- **Gráficos interativos** com Recharts
- **Interface moderna** com Material-UI
- **Responsivo** para mobile
- **Dados em tempo real** da API

---

## 🎓 Para o Workshop

### 🎯 **Demonstração Sugerida**
1. **Mostrar o processamento** dos dados (2-3 min)
2. **Iniciar backend** Django (1 min)
3. **Iniciar frontend** React (1 min)
4. **Demonstrar dashboard** completo (5 min)
5. **Focar em Criciúma** e próximos passos (3 min)

### 💡 **Pontos Chave**
- **Engenharia de Software**: Arquitetura full-stack
- **Estatística**: Análise de 1.5M registros
- **Python**: Processamento eficiente com Pandas
- **Impacto Social**: Dados para saúde pública
- **Escalabilidade**: Sistema preparado para crescimento

---

## 🚀 Próximos Passos

### 📊 **Melhorias Imediatas**
1. **Dados históricos**: Obter 2020-2023
2. **Mapas**: Integrar coordenadas GPS
3. **Bairros**: Dados geográficos de Criciúma
4. **Machine Learning**: Predição de surtos

### 🔮 **Evoluções Futuras**
1. **Dashboard público** online
2. **App mobile** para reporte
3. **Alertas automáticos** por email/SMS
4. **Integração** com sistemas de saúde

---

## 📞 Suporte

### 🐛 **Problemas Comuns**
- Verificar se todas as dependências estão instaladas
- Confirmar que ambos os servidores estão rodando
- Verificar se os dados foram processados corretamente

### 📖 **Documentação**
- **README_COMPLETO.md**: Documentação técnica detalhada
- **Código comentado**: Todos os arquivos Python/JavaScript
- **API endpoints**: Documentados em `/api/info/`

---

*Sistema desenvolvido para demonstrar o poder da Engenharia de Software + Estatística + Python em dados reais de saúde pública!* 🎉
