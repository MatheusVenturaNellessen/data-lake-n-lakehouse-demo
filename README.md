# Data Lake e Lakehouse Demo

Projeto demonstrativo de engenharia de dados que processa o conjunto `OnlineRetail.csv` em duas arquiteturas paralelas:

- **Data Lake**, com persistência em arquivos Parquet.
- **Lakehouse**, com persistência em tabelas Delta Lake.

Os dois fluxos seguem a arquitetura Medallion, dividida nas camadas **Bronze**, **Silver** e **Gold**.

## Tecnologias

- **Python**: implementação e orquestração dos pipelines.
- **Pandas**: leitura do arquivo CSV e manipulação inicial dos dados.
- **DuckDB**: transformações SQL, criação do modelo dimensional e agregações.
- **Parquet**: formato colunar utilizado pelo fluxo Data Lake.
- **Delta Lake / delta-rs**: formato transacional utilizado pelo fluxo Lakehouse.
- **PyArrow**: integração entre tabelas Delta Lake e DuckDB.
- **Bash**: execução sequencial dos dois pipelines e redirecionamento dos logs.

## Estrutura do projeto

```text
data_lake_lakehouse_demo/
├── data/
│   ├── raw/
│   │   └── OnlineRetail.csv
│   ├── lake/
│   │   ├── 01_bronze/
│   │   ├── 02_silver/
│   │   └── 03_gold/
│   └── lakehouse/
│       ├── 01_bronze/
│       ├── 02_silver/
│       └── 03_gold/
├── log/
│   └── pipeline.txt
├── src/
│   ├── lake_01_bronze.py
│   ├── lake_02_silver.py
│   ├── lake_03_gold.py
│   ├── lake_pipeline.py
│   ├── lakehouse_01_bronze.py
│   ├── lakehouse_02_silver.py
│   ├── lakehouse_03_gold.py
│   └── lakehouse_pipeline.py
├── requirements.txt
├── run_pipeline.sh
└── README.md
```

As pastas e arquivos de saída são criadas durante a execução quando necessário, incluindo a pasta `log`.

## Dependências

Exemplo de `requirements.txt` com as versões utilizadas no ambiente de desenvolvimento:

```text
pandas>=3.0.5
duckdb>=1.5.5
deltalake>=1.6.3
pyarrow>=25.0.1
```

## Pré-requisitos

- **Python 3** instalado e disponível no terminal.
- **Git Bash** ou outro ambiente compatível para executar `run_pipeline.sh`.
- Arquivo `OnlineRetail.csv` disponível em `data/raw`.

### Git Bash, Linux ou macOS

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

Em Linux ou macOS, a ativação normalmente é:

```bash
source .venv/bin/activate
```

### PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Execução

### Executar os dois pipelines

Na raiz do projeto, usando Git Bash ou outro ambiente compatível:

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

Também é possível executar sem alterar a permissão:

```bash
bash run_pipeline.sh
```

### Executar apenas o fluxo Data Lake

```bash
python ./src/lake_pipeline.py
```

### Executar apenas o fluxo Lakehouse

```bash
python ./src/lakehouse_pipeline.py
```

### Executar uma camada isoladamente

Exemplos:

```bash
python ./src/lake_01_bronze.py
python ./src/lake_02_silver.py
python ./src/lake_03_gold.py
```

A execução isolada pressupõe que as camadas anteriores já tenham produzido seus dados.

## Logs e tratamento de erros

O script `run_pipeline.sh` cria a pasta `log` e redireciona a saída normal e a saída de erro dos processos Python para:

```text
log/pipeline.txt
```

Para visualizar o arquivo no Git Bash:

```bash
cat ./log/pipeline.txt
```

Para acompanhar as últimas linhas:

```bash
tail -f ./log/pipeline.txt
```

