import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tempfile
from datetime import datetime
import os

data_execucao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
LOG_FILE = f'/home/winker/Documentos/scrapy-apps/logs/push_sheets_{data_execucao}.txt'
CREDENTIALS_FILE = '/home/winker/Documentos/scrapy-apps/credentials/credentials.json'

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
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open(spreadsheet_name).worksheet(worksheet_name)

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
    
    arquivos = {
        "apple_comments": (f"/home/winker/Documentos/scrapy-apps/archive/comentarios_{data_execucao[:10]}.csv", ";"),
        "google_rating": (f"/home/winker/Documentos/scrapy-apps/archive/google_rating_{data_execucao[:10]}.csv", ","),
        "google_star": (f"/home/winker/Documentos/scrapy-apps/archive/google_star_{data_execucao[:10]}.csv", ","),
        "apple_star": (f"/home/winker/Documentos/scrapy-apps/archive/apple_star_{data_execucao[:10]}.csv", ","),
    }
    
    arquivos_processados = {k: read_csv_file(v[0], sep=v[1]) for k, v in arquivos.items()}
    
    append_to_google_sheets(arquivos_processados["apple_comments"], "comentarios_apple_google", "apple")
    append_to_google_sheets(arquivos_processados["google_rating"], "comentarios_apple_google", "google")
    append_to_google_sheets(arquivos_processados["google_star"], "notas_downloads_apple_google", "google")
    append_to_google_sheets(arquivos_processados["apple_star"], "notas_downloads_apple_google", "apple")
    
    log_message("✅ ETL concluído!")

if __name__ == "__main__":
    etl_data()