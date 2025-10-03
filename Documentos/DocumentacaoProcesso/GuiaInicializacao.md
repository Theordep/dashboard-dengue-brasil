# Guia de Inicialização do Sistema

Este guia explica passo a passo como iniciar todos os componentes do sistema de análise de dengue, desde o processamento dos dados até a execução do frontend.

## Visão Geral

Para executar o sistema completo, você precisará de três terminais:
1. **Terminal 1**: Processamento de dados (Python)
2. **Terminal 2**: Backend (Django)
3. **Terminal 3**: Frontend (Next.js)

## Terminal 1: Processamento de Dados

Este terminal é usado para processar os dados brutos do CSV e gerar os arquivos JSON que serão consumidos pelo backend.

### Passo 1: Navegue até o diretório raiz do projeto

```bash
cd C:/ProjetoPythonDengue
```

### Passo 2: Ative o ambiente virtual (se estiver usando)

```bash
# Se estiver usando venv
# .\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### Passo 3: Execute o processador de dados básico

```bash
python data_processor.py
```

Este comando irá:
1. Carregar o arquivo `Documentos/DENGBR25.csv`
2. Processar os dados
3. Gerar o arquivo `dengue_statistics.json`

### Passo 4: Execute o processador de dados avançado (opcional)

```bash
python data_processor_advanced.py
```

ou

```bash
python scripts/run_advanced_processor.py
```

Este comando irá:
1. Carregar o arquivo `Documentos/DENGBR25.csv`
2. Processar os dados com análises avançadas
3. Gerar o arquivo `dengue_advanced_statistics.json`

**Observação**: Os passos 3 e 4 só precisam ser executados uma vez, ou quando houver atualizações no arquivo CSV de origem. Depois que os arquivos JSON forem gerados, você pode pular esses passos nas próximas inicializações do sistema.

## Terminal 2: Backend (Django)

Este terminal é usado para executar o servidor Django que fornece a API REST.

### Passo 1: Navegue até o diretório do backend

```bash
cd C:/ProjetoPythonDengue/backend
```

### Passo 2: Ative o ambiente virtual (se estiver usando)

```bash
# Se estiver usando venv
# .\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### Passo 3: Execute as migrações (se for a primeira vez)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Passo 4: Inicie o servidor Django

```bash
python manage.py runserver
```

Este comando iniciará o servidor Django na porta 8000. Você deverá ver uma saída semelhante a:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 03, 2025 - 14:05:06
Django version 5.2.7, using settings 'denguedashboard.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Passo 5: Carregue os dados no banco de dados (se for a primeira vez)

Em outro terminal ou em um navegador, acesse:

```
http://localhost:8000/api/carregar-estatisticas/
```

E, se estiver usando estatísticas avançadas:

```
http://localhost:8000/api/avancado/carregar-estatisticas/
```

Esses endpoints carregarão os dados dos arquivos JSON para o banco de dados SQLite.

## Terminal 3: Frontend (Next.js)

Este terminal é usado para executar o servidor de desenvolvimento do Next.js que fornece a interface do usuário.

### Passo 1: Navegue até o diretório do frontend

```bash
cd C:/ProjetoPythonDengue/frontend/dengue
```

### Passo 2: Instale as dependências (se for a primeira vez)

```bash
npm install
```

### Passo 3: Inicie o servidor de desenvolvimento do Next.js

```bash
npm run dev
```

Este comando iniciará o servidor Next.js na porta 3000. Você deverá ver uma saída semelhante a:

```
> dengue@0.1.0 dev
> next dev
   ▲ Next.js 15.5.4
   - Local:        http://localhost:3000
   - Network:      http://172.28.176.1:3000
 ✓ Ready in 5.7s
```

## Acessando o Sistema

Uma vez que todos os três componentes estejam em execução:

1. O backend estará disponível em: `http://localhost:8000/api/`
2. O frontend estará disponível em: `http://localhost:3000/`

Você pode acessar o frontend no seu navegador e começar a explorar o dashboard de dengue.

## Resumo dos Comandos

Para iniciar rapidamente o sistema, aqui está um resumo dos comandos principais:

### Terminal 1 (Processamento - apenas na primeira vez)
```bash
cd C:/ProjetoPythonDengue
python data_processor.py
python data_processor_advanced.py
```

### Terminal 2 (Backend)
```bash
cd C:/ProjetoPythonDengue/backend
python manage.py runserver
```

### Terminal 3 (Frontend)
```bash
cd C:/ProjetoPythonDengue/frontend/dengue
npm run dev
```

## Solução de Problemas

### O frontend não consegue se conectar ao backend

Verifique se:
- O servidor Django está em execução na porta 8000
- Não há problemas de CORS (Cross-Origin Resource Sharing)
- O frontend está configurado para acessar a URL correta do backend (`http://localhost:8000/api/`)

### Os dados não aparecem no dashboard

Verifique se:
1. Os arquivos JSON foram gerados corretamente
2. Os dados foram carregados no banco de dados usando os endpoints de carregamento
3. Não há erros no console do navegador

### Erro ao processar os dados

Verifique se:
1. O arquivo CSV está no local correto (`Documentos/DENGBR25.csv`)
2. Você tem permissões para ler o arquivo
3. O arquivo está no formato correto

### Erro ao iniciar o backend

Verifique se:
1. Todas as dependências Python estão instaladas (`pip install -r requirements.txt`)
2. As migrações do Django foram aplicadas
3. A porta 8000 não está sendo usada por outro processo

### Erro ao iniciar o frontend

Verifique se:
1. Todas as dependências Node.js estão instaladas (`npm install`)
2. A porta 3000 não está sendo usada por outro processo
3. A versão do Node.js é compatível com o Next.js (recomendado: Node.js 20+)
