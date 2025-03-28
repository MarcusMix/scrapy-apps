import subprocess
import os
from datetime import datetime

# Obtém o caminho base do projeto (assumindo que o script roda na raiz do repositório)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Caminho para o log (relativo ao diretório do projeto)
data_execucao = datetime.now().date()
log_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(log_dir, exist_ok=True)  # Garante que a pasta exista
log_file = os.path.join(log_dir, f"execucao_{data_execucao}.txt")

def registrar_log(mensagem):
    with open(log_file, "a") as log:
        log.write(mensagem + "\n")
    print(mensagem)

def fetch_API_itunes():
    registrar_log("Executando a função *fetch_API_itunes*")
    data_dir = os.path.join(BASE_DIR, "data/api_itunes")
    os.chdir(data_dir)
    registrar_log(f"Diretório atual: {os.getcwd()}")

    result = subprocess.run(["python", "api_consumer_itunes.py"], capture_output=True, text=True)

    if result.returncode == 0:
        registrar_log("*fetch_API_itunes* executado com sucesso!")
    else:
        registrar_log(f"Erro ao executar *fetch_API_itunes*: {result.stderr}")
        raise Exception(f"Erro ao executar *fetch_API_itunes*: {result.stderr}")

def fetch_webscraping_google_star():
    registrar_log("Executando a função *fetch_webscraping_google_star*")
    data_dir = os.path.join(BASE_DIR, "data/webscraping/googlewebscraping/spiders")
    os.chdir(data_dir)
    registrar_log(f"Diretório atual: {os.getcwd()}")

    output_path = os.path.join(BASE_DIR, "archive", f"google_star_{data_execucao}.csv")
    result = subprocess.run(["scrapy", "crawl", "google_star", "-o", output_path], capture_output=True, text=True)

    if result.returncode == 0:
        registrar_log("*fetch_webscraping_google_star* executado com sucesso!")
    else:
        registrar_log(f"Erro ao executar *fetch_webscraping_google_star*: {result.stderr}")
        raise Exception(f"Erro ao executar *fetch_webscraping_google_star*: {result.stderr}")

def fetch_webscraping_apple_star():
    registrar_log("Executando a função *fetch_webscraping_apple_star*")
    data_dir = os.path.join(BASE_DIR, "data/webscraping/googlewebscraping/spiders")
    os.chdir(data_dir)
    registrar_log(f"Diretório atual: {os.getcwd()}")

    output_path = os.path.join(BASE_DIR, "archive", f"apple_star_{data_execucao}.csv")
    result = subprocess.run(["scrapy", "crawl", "apple_star", "-o", output_path], capture_output=True, text=True)

    if result.returncode == 0:
        registrar_log("*fetch_webscraping_apple_star* executado com sucesso!")
    else:
        registrar_log(f"Erro ao executar *fetch_webscraping_apple_star*: {result.stderr}")
        raise Exception(f"Erro ao executar *fetch_webscraping_apple_star*: {result.stderr}")

def fetch_webscraping_google_rating():
    registrar_log("Executando a função *fetch_webscraping_google_rating*")
    data_dir = os.path.join(BASE_DIR, "data/webscraping/googlewebscraping/spiders")
    os.chdir(data_dir)
    registrar_log(f"Diretório atual: {os.getcwd()}")

    output_path = os.path.join(BASE_DIR, "archive", f"google_rating_{data_execucao}.csv")
    result = subprocess.run(["scrapy", "crawl", "google_rating", "-o", output_path], capture_output=True, text=True)

    if result.returncode == 0:
        registrar_log("*fetch_webscraping_google_rating* executado com sucesso!")
    else:
        registrar_log(f"Erro ao executar *fetch_webscraping_google_rating*: {result.stderr}")
        raise Exception(f"Erro ao executar *fetch_webscraping_google_rating*: {result.stderr}")

def main():
    try:
        registrar_log(f"\n--- Execução iniciada em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

        fetch_API_itunes()
        fetch_webscraping_google_rating()
        fetch_webscraping_google_star()
        fetch_webscraping_apple_star()

        registrar_log("\nTodos os processos foram executados com sucesso!\n")

    except Exception as e:
        registrar_log(f"\nOcorreu um erro durante a execução: {str(e)}\n")

    finally:
        registrar_log(f"--- Execução finalizada em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

if __name__ == "__main__":
    main()
