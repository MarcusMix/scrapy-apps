import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tempfile
import json
from datetime import datetime

# Obtém a data atual para logs
data_execucao = datetime.now().date()

# Caminho para o diretório atual
BASE_DIR = os.getcwd()  # Diretório atual de execução

# Caminho para as pastas de logs e archive
LOG_DIR = os.path.join(BASE_DIR, 'logs')
ARCHIVE_DIR = os.path.join(BASE_DIR, 'archive')

# Caminho para o arquivo de log
LOG_FILE = os.path.join(LOG_DIR, f'push_sheets_{data_execucao}.txt')

# Carrega as credenciais do Google Sheets
CREDENTIALS_JSON = os.getenv("GOOGLE_SHEETS_CREDENTIALS")

# Função para registrar mensagens no log
def log_message(message):
    """Registra uma mensagem no arquivo de log."""
    with open(LOG_FILE, 'a') as log:
        log.write(f"[{data_execucao}] {message}\n")

def read_csv_file(file_path, sep=","):
    """Lê um arquivo CSV e retorna um caminho temporário para processamento."""
    try:
        df = pd.read_csv(file_path, sep=sep)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        df.to_csv(temp_file.name, index=False)
        log_message(f"SUCESSO: Leitura do arquivo {file_path}")
        return temp_file.name
    except Exception as e:
        log_message(f"ERRO: Falha ao ler o arquivo {file_path} - {str(e)}")
        return None

def append_to_google_sheets(file_path, spreadsheet_name, worksheet_name):
    """Adiciona os dados do CSV ao Google Sheets."""
    if file_path is None:
        return
    try:
        # Usar as credenciais do JSON
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(CREDENTIALS_JSON), ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
        client = gspread.authorize(creds)
        sheet = client.open(spreadsheet_name).worksheet(worksheet_name)
        sheets = client.open(spreadsheet_name)
        log_message(f"Planilhas disponíveis: {[sheet.title for sheet in sheets.worksheets()]}")

        df = pd.read_csv(file_path).fillna('')
        data = df.values.tolist()
        last_row = len(sheet.col_values(1)) + 1
        chunk_size = max(1, len(data) // 5)
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

        for chunk in chunks:
            sheet.append_rows(chunk, value_input_option="RAW", table_range=f"A{last_row}")
            last_row += len(chunk)
        
        log_message(f"SUCESSO: Dados de {file_path} enviados para {spreadsheet_name} - {worksheet_name}")
    except Exception as e:
        log_message(f"ERRO: Falha ao enviar dados de {file_path} para {spreadsheet_name} - {worksheet_name} - {str(e)}")

def etl_data():
    """Executa todo o processo de ETL na sequência correta."""
    log_message("🔄 Iniciando ETL...")
    
    # Usando caminhos relativos para os arquivos na pasta 'archive'
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