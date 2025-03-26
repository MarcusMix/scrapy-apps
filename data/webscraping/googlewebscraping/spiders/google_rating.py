import scrapy
import time
import re
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from googlewebscraping.functions.url_google import all_url_google
from googlewebscraping.functions.format_date import format_date
from googlewebscraping.functions.web_driver import web_driver

class MySpider(scrapy.Spider):
    name = "google_rating"
    start_urls = all_url_google()

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.driver = web_driver()
        self.contador_erros = 0
        self.contador_sucessos = 0
        self.data_limite = datetime.now() - timedelta(days=100)
    
    def parse(self, response):
        self.driver.get(response.url)

        try:
            botao_classificacoes = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/c-wiz[5]/section/header/div/div[2]/button'))
            )
            # //*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/c-wiz[5]/section/header/div/div[2]/button
            # //*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/c-wiz[4]/section/header/div/div[2]/button
            botao_classificacoes.click()
        except:
            print("O botao_classificacoes não ficou clicável a tempo.")
            self.contador_erros += 1
            print(f"Erros até o momento: {self.contador_erros}")

        try:
            combobox_avaliacoes =  WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="sortBy_1"]/div[2]'))
            ) 
            combobox_avaliacoes.click()
        except:
            print("O combobox_avaliacoes não ficou clicável a tempo.")
            
        time.sleep(2)
        try:
            mais_recentes = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='menu']//span[contains(@aria-label, 'Mais recentes')]"))
            )
            mais_recentes.click()
        except:
            print("O mais_recentes não ficou clicável a tempo.")

        time.sleep(2)
        html = self.driver.page_source
        sel_response = scrapy.Selector(text=html)

        self.contador_sucessos += 1

        page_name = sel_response.css('span.AfwdI::text').get()
        # page_name = sel_response.css('h1.Fd93Bb::text').get()
        for item in sel_response.css('div.RHo1pe'):
            div_star = item.css('div.iXRFPc')
            if div_star:
                star_text = div_star.xpath('@aria-label').get()
                star = re.search(r'\d', star_text).group() if star_text else None
                
            response_div = item.xpath('.//div[@class="ras4vb"]/div')
            response_text = response_div.xpath('string(.)').get()
            
            # GRAVA SOMENTE COMENTÁRIOS APÓS A ÚLTIMA DATA DE VERIFICAÇÃO!
            comment_date_text = item.css('span.bp9Aid::text').get()
            comment_date_str = format_date(comment_date_text)
            comment_date = datetime.strptime(comment_date_str, '%d/%m/%Y')

            if comment_date and comment_date > self.data_limite:
                yield {
                    'app_name' : page_name,
                    'plataforma' : 'google',
                    'user_reviewer': item.css('div.X5PpBb::text').get(),
                    'date': format_date(item.css('span.bp9Aid::text').get()),
                    # stars PARA FLOAT
                    'stars': float(star),
                    'commentary' : item.css('div.h3YV2d::text').get(),
                    'user_response' : item.css('div.I6j64d::text').get(),
                    'date_response' : format_date(item.css('div.I9Jtec::text').get()) if item.css('div.I9Jtec::text').get() else None,
                    'response' : response_text
                }

    def closed(self, reason):
        print(f"Total de erros na varredura: {self.contador_erros}")
        print(f"Total de sucesso na varredura: {self.contador_sucessos}")
        self.driver.quit()
