# 🐍 Projeto de Coleta e Envio de Dados

Este projeto utiliza um ambiente virtual para isolar as dependências e executa dois scripts principais:

- `run_scrappers.py`: responsável por realizar o scraping dos dados
- `push_sheets.py`: responsável por enviar os dados para o Google Sheets

---

## ✅ Pré-requisitos

- Python 3.x instalado na máquina

---

## 🚀 Como rodar o projeto

### 1. Criar o ambiente virtual (caso não exista)

```bash
python -m venv env
```

---

### 2. Ativar o ambiente virtual

**Linux/macOS:**

```bash
source env/bin/activate
```

**Windows (cmd):**

```cmd
env\Scripts\activate
```

**Windows (PowerShell):**

```powershell
.\env\Scripts\Activate.ps1
```

---

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Executar os scripts

#### 🕷️ Scraping de dados

```bash
python script/run_scrappers.py
```

#### 📤 Envio para Google Sheets

```bash
python script/push_sheets.py
```

---

### 5. Sair do ambiente virtual

```bash
deactivate
```

---

## 🗂️ Estrutura do projeto

```bash
scrappy-apps/
├── env/    
├── arquive/                 # Arquivos gerados 
├── credentials/             # Configuração de credenciais
├── data/                    # Webscrappers e API consumers
├── script/
│   ├── run_scrappers.py     # Script de scraping
│   └── push_sheets.py       # Script de envio para planilhas
├── requirements.txt         # Lista de dependências
├── run_scripts.sh           # Script para rodar os scripts
└── README.md                # Este arquivo
```

---

## 📌 Observações

- A pasta `env/` deve ser ignorada no Git. Adicione isso ao `.gitignore`:

```bash
# .gitignore
env/
```