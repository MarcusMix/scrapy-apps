import subprocess
import os
from datetime import datetime

data_execucao = datetime.now().date()
log_file = f"/home/winker/Documentos/scrapy-apps/logs/execucao_{data_execucao}.txt"

def registrar_log(mensagem):
    with open(log_file, "a") as log:
        log.write(mensagem + "\n")
    print(mensagem)

def fetch_API_itunes():
    registrar_log("Executando a função *fetch_API_itunes*")
    data_dir = "/home/winker/Documentos/scrapy-apps/data/api_itunes"
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
    data_dir = "/home/winker/Documentos/scrapy-apps/data/webscraping/googlewebscraping/spiders"
    os.chdir(data_dir)
    registrar_log(f"Diretório atual: {os.getcwd()}")

    result = subprocess.run(
        ["scrapy", "crawl", "google_star", "-o", f"/home/winker/Documentos/scrapy-apps/archive/google_star_{data_execucao}.csv"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        registrar_log("*fetch_webscraping_google_star* executado com sucesso!")
    else:
        registrar_log(f"Erro ao executar *fetch_webscraping_google_star*: {result.stderr}")
        raise Exception(f"Erro ao executar *fetch_webscraping_google_star*: {result.stderr}")

def fetch_webscraping_apple_star():
    registrar_log("Executando a função *fetch_webscraping_apple_star*")
    data_dir = "/home/winker/Documentos/scrapy-apps/data/webscraping/googlewebscraping/spiders"
    os.chdir(data_dir)
    registrar_log(f"Diretório atual: {os.getcwd()}")

    result = subprocess.run(
        ["scrapy", "crawl", "apple_star", "-o", f"/home/winker/Documentos/scrapy-apps/archive/apple_star_{data_execucao}.csv"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        registrar_log("*fetch_webscraping_apple_star* executado com sucesso!")
    else:
        registrar_log(f"Erro ao executar *fetch_webscraping_apple_star*: {result.stderr}")
        raise Exception(f"Erro ao executar *fetch_webscraping_apple_star*: {result.stderr}")

def fetch_webscraping_google_rating():
    registrar_log("Executando a função *fetch_webscraping_google_rating*")
    data_dir = "/home/winker/Documentos/scrapy-apps/data/webscraping/googlewebscraping/spiders"
    os.chdir(data_dir)
    registrar_log(f"Diretório atual: {os.getcwd()}")

    result = subprocess.run(
        ["scrapy", "crawl", "google_rating", "-o", f"/home/winker/Documentos/scrapy-apps/archive/google_rating_{data_execucao}.csv"],
        capture_output=True, text=True
    )

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
    os.makedirs("/home/winker/Documentos/scrapy-apps/logs", exist_ok=True)
    main()