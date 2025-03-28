import pandas as pd
import requests
import json
from datetime import datetime, timedelta

page_n = "1"
country = "br"
data_execucao = datetime.now().date()

# Carregando informações dos apps
with open('/home/winker/Documentos/scrapy-apps/credentials/ids.json', 'r') as file_id:
    data_apps = json.load(file_id)

autores = []
datas = []
stars = []
titulos = []
comentarios = []
app_name = []

data_limite = datetime.now() - timedelta(days=7)

def format_iso_date(data_comentario):
    try:
        date_obj = datetime.fromisoformat(data_comentario)
        date_formatted = date_obj.strftime("%d/%m/%Y")
        return date_formatted
    except Exception as e:
        print(f"Erro ao formatar a data: {e}")
        return data_comentario
    
def format_data(data_comentario):
    date_obj = datetime.fromisoformat(data_comentario)
    date_only = date_obj.date()
    datetime_with_date_only = datetime.combine(date_only, datetime.min.time())
    return datetime_with_date_only


def api():
    for app in data_apps:
        url = f"http://itunes.apple.com/rss/customerreviews/page={page_n}/id={app['id']}/sortby=mostrecent/json?cc={country}"
        response = requests.get(url)
        print(f"INICIANDO APP {app['id']} {app['name']}")

        if response.status_code == 200:
            data = response.json()

            if 'feed' in data and 'entry' in data['feed']:
                entries = data['feed']['entry']

                if isinstance(entries, list):
                    for comentario in entries:
                        autor = comentario['author']['name']['label']
                        data_comentario = comentario['updated']['label']
                        star = comentario['im:rating']['label']
                        title = comentario['title']['label']
                        content = comentario['content']['label']
                        
                        print(f"Autor: {autor}, título: {title}, comentário: {content}, data: {format_iso_date(data_comentario)}, nota: {star}")

                        # GRAVA SOMENTE COMENTÁRIOS APÓS A ÚLTIMA DATA DE VERIFICAÇÃO!
                        data_comentario_formatada = format_data(data_comentario)

                        if data_comentario_formatada and data_comentario_formatada > data_limite:
                            autores.append(autor)
                            datas.append(format_iso_date(data_comentario))
                            # TESTE DE CASTING DE star PARA FLOAT
                            stars.append(float(star))
                            titulos.append(title)
                            comentarios.append(content)
                            app_name.append(app["name"])
                else:
                    print(f"Nenhum comentário encontrado para o app: {app['name']}")
            else:
                print(f"Nenhum comentário encontrado para o app: {app['name']}")
        else:
            print(f"Erro na requisição para o app {app['name']}: {response.status_code}")

    df = pd.DataFrame({
        'app_name': app_name,
        'plataforma' : 'apple',
        'user_reviewer': autores,
        'date': datas,
        'stars': stars,
        # 'Título': titulos,
        'commentary': comentarios
    })

    df.to_csv(f'/home/winker/Documentos/scrapy-apps/archive/comentarios_{data_execucao}.csv', sep=";", index=False)

    print(f"Processo concluído. Comentários exportados para comentarios_{data_execucao}.csv.")


if __name__ == "__main__":
    api()