import csv
import threading
import random
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import logging

class Scraper:
    def __init__(self, output_file, security_url, technology_url, sports_url, food_url, counts=10):
        self.security_url = security_url
        self.technology_url = technology_url
        self.sports_url = sports_url
        self.food_url = food_url
        self.output_file = output_file
        self.counts = counts
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
        ]

        logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def write_to_csv(self, data):
        try:
            with open(self.output_file, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['title', 'url', 'text']  # Estructura del CSV: título, URL, texto
                # Configurar el delimitador y el encoding
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

                # Si el archivo está vacío, escribe la cabecera
                if csvfile.tell() == 0:
                    writer.writeheader()

                # Agrega la nueva fila al archivo
                writer.writerow({
                    'title': data['title'],
                    'url': data['url'],
                    'text': data['text']
                })
        except Exception as e:
            logging.error(f"Error al escribir en el archivo CSV: {e}")

    def scrape_security_news(self):
        try:
            headers = {'User-Agent': self.get_random_user_agent()}
            response = requests.get(self.security_url, headers=headers)
            pass
        except Exception as e:
            logging.error(f"Error al obtener noticias de seguridad: {e}")

    def scrape_technology_news(self):
        try:
            headers = {'User-Agent': self.get_random_user_agent()}
            response = requests.get(self.technology_url, headers=headers)
            pass
        except Exception as e:
            logging.error(f"Error al obtener noticias de tecnología: {e}")

    def scrape_sports_news(self):
        try:
            headers = {'User-Agent': self.get_random_user_agent()}
            response = requests.get(self.sports_url, headers=headers)
            pass
        except Exception as e:
            logging.error(f"Error al obtener noticias de deportes: {e}")

    def scrape_food_news(self):
        try:
            headers = {'User-Agent': self.get_random_user_agent()}
            response = requests.get(self.food_url, headers=headers)
            if response.status_code == 200:
                root = ET.fromstring(response.content)

                url_list = []
                for url_elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
                    loc_elem = url_elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                    if loc_elem is not None:
                        url_list.append(loc_elem.text)

                for url in url_list[1:self.counts]:
                    headers = {'User-Agent': self.get_random_user_agent()}
                    response_url = requests.get(url, headers=headers)
                    if response_url.status_code == 200:
                        soup = BeautifulSoup(response_url.text, 'html.parser')

                        div_with_classes = soup.find('div', class_='container container--no-padding-md')
                        if div_with_classes:
                            paragraphs = div_with_classes.find_all('p')
                            titulo = soup.h1.text
                            titulo = titulo.replace('\n', '')
                            texto = ''
                            for paragraph in paragraphs:
                                texto += paragraph.text
                            texto = texto.replace('\n', '')
                            self.write_to_csv({
                                'title': titulo,
                                'url': url,
                                'text': texto
                            })
                        else:
                            logging.warning(f"Div with classes not found in {url}")
                    else:
                        logging.error(f"Failed to retrieve {url}. Status code: {response_url.status_code}")
        except Exception as e:
            logging.error(f"Error en la función de scraping de noticias de comida: {e}")

    def run_scrapers(self):
        # Crear hilos para ejecutar cada scraper
        threads = []
        #threads.append(threading.Thread(target=self.scrape_security_news))
        #threads.append(threading.Thread(target=self.scrape_technology_news))
        #threads.append(threading.Thread(target=self.scrape_sports_news))
        threads.append(threading.Thread(target=self.scrape_food_news))

        # Iniciar los hilos
        for thread in threads:
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()
