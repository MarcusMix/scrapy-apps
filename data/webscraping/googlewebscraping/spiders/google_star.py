import scrapy
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

from googlewebscraping.functions.web_driver import web_driver
from googlewebscraping.functions.url_google import all_url_google

class MySpider(scrapy.Spider):
    name = "google_star"
    start_urls = all_url_google()

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.driver = web_driver()
    
    def parse(self, response):
        self.driver.get(response.url)
        html = self.driver.page_source
        sel_response = scrapy.Selector(text=html)

        # page_name = sel_response.css('h1.Fd93Bb::text').get()
        page_name = sel_response.css('span.AfwdI::text').get()

        star = sel_response.css('div.TT9eCd::text').get()
        avaliacoes_totais_raw = sel_response.css('div.g1rdde::text').get()
        downloads_totais_raw = sel_response.css('div.ClM7O::text').get()

        def clean_avaliacoes(avaliacoes):
            if avaliacoes != 'Downloads':
                if 'mil' in avaliacoes:
                    multiplier = 10
                elif 'milhão' in avaliacoes:
                    multiplier = 10000
                else:
                    multiplier = 1
                # Usando regex para encontrar todos os dígitos e vírgulas
                numbers = re.findall(r'[\d,]+', avaliacoes)
                # Juntar os números em uma única string, remover vírgulas e converter para inteiro
                num_str = ''.join(numbers).replace(',', '')
                return int(num_str) * multiplier
            else:
                avaliacoes == 0
            return 0
        
        def clean_downloads(downloads):
            if downloads:
                downloads = downloads.replace('mil+', '000').replace('+', '').replace('mil', '000')
                return int(re.sub(r'[^0-9]', '', downloads))
            return 0
        
        avaliacoes_totais = clean_avaliacoes(avaliacoes_totais_raw)
        downloads_totais = clean_downloads(downloads_totais_raw)

        yield {
            'app_name': page_name,
            'data': datetime.now().date(),
            'star': star,
            'avaliacoes_totais': avaliacoes_totais,
            'downloads_totais': downloads_totais,
        }

    def closed(self, reason):
        self.driver.quit()
