# Dashboard de Dengue - Brasil

Análise epidemiológica com dados do DATASUS.

## Estrutura do Projeto

- **backend/**: API Django com endpoints para dados de dengue
- **frontend/dengue/**: Interface web em Next.js e Tailwind CSS
- **data_processor.py**: Processador de dados do CSV para JSON
- **data_processor_advanced.py**: Processador avançado com métricas adicionais
- **data_processor_fixed.py**: Versão corrigida do processador avançado
- **scripts/**: Scripts utilitários
- **documentacao/**: Documentação detalhada do projeto
- **Documentos/**: Arquivos de dados e dicionários
- **arquivos_obsoletos/**: Arquivos antigos mantidos para referência

## Fluxo de Dados

1. **Leitura e Processamento**: O CSV é processado por `data_processor.py` ou `data_processor_advanced.py`
2. **Armazenamento**: Os dados processados são salvos em arquivos JSON
3. **Backend**: A API Django carrega os dados JSON para o banco de dados
4. **Frontend**: A interface web consome os dados da API

## Requisitos

- Python 3.13+
- Django 5.2+
- Node.js 20+
- Next.js 15+

## Instalação

```bash
# Instalar dependências Python
pip install -r requirements.txt

# Instalar dependências Node.js
cd frontend/dengue
npm install
```

## Execução

### Processamento de Dados

```bash
# Processamento básico
python data_processor.py

# Processamento avançado
python scripts/run_advanced_processor.py
```

### Backend

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend/dengue
npm run dev
```

## Documentação

Para documentação detalhada, consulte os arquivos em `documentacao/`:

- **COMO_USAR.md**: Instruções detalhadas de uso
- **README_COMPLETO.md**: Documentação completa do projeto
- **relatorio_final_dengue.md**: Relatório de análise dos dados

## Funcionalidades

- Dashboard com estatísticas gerais
- Análise por estado brasileiro
- Análise temporal de casos
- Análise de sintomas mais comuns
- Detalhamento para Santa Catarina
- Análise avançada (faixa etária, gênero, etc.)