import scrapy
import re
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from googlewebscraping.functions.url_apple import all_url_apple
from googlewebscraping.functions.web_driver import web_driver

class MySpider(scrapy.Spider):
    name = "apple_star"
    start_urls = all_url_apple()

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.driver = web_driver()
        self.contador_erros = 0
        self.contador_sucessos = 0
    
    def parse(self, response):
        self.driver.get(response.url)

        # time.sleep(2)
        html = self.driver.page_source
        sel_response = scrapy.Selector(text=html)

        self.contador_sucessos += 1

        page_name = sel_response.css('h1.product-header__title::text').get()
        star = sel_response.css('span.we-customer-ratings__averages__display::text').get()
        avaliacoes_totais = sel_response.css('p.we-customer-ratings__count::text').get()

        # Função para extrair apenas números de uma string
        def extract_numbers(text):
            # Verifica se o texto contém "mil" ou "milhão"
            if 'mil' in text:
                multiplier = 1000
            elif 'milhão' in text:
                multiplier = 1000000
            else:
                multiplier = 1

            num_str = text.replace('.', '').replace(',', '.')
    
            # Usar regex para encontrar todos os dígitos e pontos
            numbers = re.findall(r'[\d.]+', num_str)
            
            # Juntar os números em uma única string e converter para float para lidar com valores decimais
            num_str = ''.join(numbers)
            return int(float(num_str) * multiplier)

        if avaliacoes_totais:
            avaliacoes_totais = extract_numbers(avaliacoes_totais)

        print(page_name, star, avaliacoes_totais)

        yield {
            'app_name' : page_name.strip(),
            'date': datetime.now().date(),
            'star': star,
            'avaliacoes_totais' : avaliacoes_totais
        }

    def closed(self, reason):
        print(f"Total de erros na varredura: {self.contador_erros}")
        print(f"Total de sucesso na varredura: {self.contador_sucessos}")
        self.driver.quit()
