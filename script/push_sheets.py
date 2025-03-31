import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tempfile
import json
from datetime import datetime

# Obtém a data atual formatada
data_execucao = datetime.now().strftime("%Y-%m-%d")

# Caminho para o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Garante que a pasta de logs existe
os.makedirs(LOG_DIR, exist_ok=True)

# Caminho para o arquivo de log
LOG_FILE = os.path.join(LOG_DIR, f'push_sheets_{data_execucao}.txt')

# Carrega as credenciais do Google Sheets
CREDENTIALS_JSON = os.getenv("GOOGLE_SHEETS_CREDENTIALS")


# Função para registrar mensagens no log e no terminal
def log_message(message):
    """Registra uma mensagem no arquivo de log e exibe no terminal."""
    log_entry = f"[{data_execucao}] {message}"
    print(log_entry)  # Exibe no terminal
    with open(LOG_FILE, 'a') as log:
        log.write(log_entry + "\n")


def read_csv_file(file_path, sep=","):
    """Lê um arquivo CSV e retorna um caminho temporário para processamento."""
    try:
        print(f"📂 Verificando arquivo: {file_path}")

        # Verifica se o arquivo está vazio antes de abrir
        if os.path.getsize(file_path) == 0:
            log_message(f"⚠️ Arquivo {file_path} está vazio. Pulando...")
            return None

        df = pd.read_csv(file_path, sep=sep)

        # Verifica se tem colunas válidas
        if df.empty or df.columns.size == 0:
            log_message(f"⚠️ Arquivo {file_path} não contém colunas válidas. Pulando...")
            return None

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        df.to_csv(temp_file.name, index=False)

        log_message(f"✅ SUCESSO: Leitura do arquivo {file_path}")
        return temp_file.name
    except Exception as e:
        log_message(f"❌ ERRO: Falha ao ler o arquivo {file_path} - {str(e)}")
        return None


def append_to_google_sheets(file_path, spreadsheet_name, worksheet_name):
    """Adiciona os dados do CSV ao Google Sheets."""
    if file_path is None:
        log_message(f"⚠️ Arquivo não encontrado. Pulando {worksheet_name}...")
        return

    # Verifica se as credenciais estão definidas corretamente
    if not CREDENTIALS_JSON:
        log_message("❌ ERRO: Variável de ambiente GOOGLE_SHEETS_CREDENTIALS não está definida!")
        return

    try:
        print(f"🔑 Tentando autenticação no Google Sheets...")
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(CREDENTIALS_JSON),
                                                                 ["https://spreadsheets.google.com/feeds",
                                                                  "https://www.googleapis.com/auth/drive"])
        client = gspread.authorize(creds)
        sheet = client.open(spreadsheet_name).worksheet(worksheet_name)

        print(f"📊 Enviando dados para {spreadsheet_name} - {worksheet_name}")

        df = pd.read_csv(file_path).fillna('')
        data = df.values.tolist()
        last_row = len(sheet.col_values(1)) + 1

        if not data:
            log_message(f"⚠️ Nenhum dado encontrado em {file_path}. Pulando...")
            return

        chunk_size = max(1, len(data) // 5)
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

        for chunk in chunks:
            sheet.append_rows(chunk, value_input_option="RAW", table_range=f"A{last_row}")
            last_row += len(chunk)

        log_message(f"✅ SUCESSO: Dados de {file_path} enviados para {spreadsheet_name} - {worksheet_name}")

    except Exception as e:
        log_message(f"❌ ERRO: Falha ao enviar dados de {file_path} para {spreadsheet_name} - {worksheet_name} - {str(e)}")


def etl_data():
    """Executa todo o processo de ETL na sequência correta."""
    log_message("🔄 Iniciando ETL...")
    
    # Listando arquivos no diretório archive
    print(f"📂 Listando arquivos no diretório: {ARCHIVE_DIR}")
    print(f"📃 Arquivos encontrados: {os.listdir(ARCHIVE_DIR)}")

    # Usando caminhos com data_execucao nos nomes dos arquivos
    arquivos = {
        "apple_comments": (os.path.join(ARCHIVE_DIR, f"comentarios_{data_execucao}.csv"), ";"),
        "google_rating": (os.path.join(ARCHIVE_DIR, f"google_rating_{data_execucao}.csv"), ","),
        "google_star": (os.path.join(ARCHIVE_DIR, f"google_star_{data_execucao}.csv"), ","),
        "apple_star": (os.path.join(ARCHIVE_DIR, f"apple_star_{data_execucao}.csv"), ","),
    }

    arquivos_processados = {k: read_csv_file(v[0], sep=v[1]) for k, v in arquivos.items()}

    append_to_google_sheets(arquivos_processados["apple_comments"], "comentarios_apple_google", "apple")
    append_to_google_sheets(arquivos_processados["google_rating"], "comentarios_apple_google", "google")
    append_to_google_sheets(arquivos_processados["google_star"], "notas_downloads_apple_google", "google")
    append_to_google_sheets(arquivos_processados["apple_star"], "notas_downloads_apple_google", "apple")

    log_message("✅ ETL concluído!")


if __name__ == "__main__":
    etl_data()