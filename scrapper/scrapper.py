import csv
import threading
import random
import re

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import logging


def get_random_user_agent():
    """
        Obtiene un User-Agent aleatorio de la lista de User-Agents.
        Returns:
            str: User-Agent aleatorio.
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110'
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100'
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97'
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116'
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97'
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116'
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110'
        ' Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 S'
        'afari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97'
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 '
        'Safari/537.36',
    ]
    return random.choice(user_agents)


class Scraper:
    def __init__(self, output_file, security_url, cars_url, sports_url, food_url, counts=1):
        """
        constructor de la clase Scraper con las URLs de los sitios a trabajar.

        Args:
            output_file (str): Nombre del archivo CSV de salida.
            security_url (str): URL de noticias de seguridad .xml.
            cars_url (str): URL de noticias de autos.
            sports_url (str): URL de noticias de deportes.
            food_url (str): URL de noticias de comida .
            counts (int): Número de noticias a raspar.
        """
        self.security_url = security_url
        self.cars_url = cars_url
        self.sports_url = sports_url
        self.food_url = food_url
        self.output_file = output_file
        self.counts = counts
        self.user_agent = get_random_user_agent()

        logging.basicConfig(filename='scraper.log', level=logging.INFO,
                            format='%(asctime)s [%(levelname)s]: %(message)s')

    def write_to_csv(self, data):
        """
        Escribe datos en el archivo CSV de salida.

        Args:
            data (dict): Datos a escribir en el CSV (título, URL, texto).
        """
        try:
            with open(self.output_file, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['title', 'url', 'text', 'category']  # Estructura del CSV: título, URL, texto
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')

                if csvfile.tell() == 0:
                    writer.writeheader()
                text_cleaned = data['text'].strip().replace(',', '').replace('.', '').replace(';', '')
                writer.writerow({
                    'title': data['title'],
                    'url': data['url'],
                    'text': text_cleaned,
                    'category': data['category']
                })
        except Exception as e:
            logging.error(f"Error al escribir en el archivo CSV: {e}")

    def scrape_security_news(self):
        """
        scrapper noticias de seguridad y las escribe en el archivo CSV
        """
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(self.security_url, headers=headers, stream=True)
            sub_sitemap = []
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                locs = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                for loc in locs:
                    sub_sitemap.append(loc.text)
                    break
                url_links = []
                for site_map in sub_sitemap:
                    headers = {'User-Agent': self.user_agent}
                    response_sitemap = requests.get(site_map, headers=headers, stream=True)
                    if response_sitemap.status_code == 200:
                        root_map = ET.fromstring(response_sitemap.text)
                        locs = root_map.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                        for loc in locs:
                            url_links.append(loc.text)

                for link in url_links[1:self.counts]:
                    headers = {'User-Agent': self.user_agent}
                    response_url = requests.get(link, headers=headers, stream=True)
                    if response_url.status_code == 200:
                        soup = BeautifulSoup(response_url.text, 'html.parser')
                        title = soup.find('h2', class_='post-title entry-title')
                        if title:
                            title = title.text.replace('\n', '').lstrip()
                        else:
                            title = "No title found"
                        div_with_classes = soup.find('div', class_='post-body entry-content')
                        if div_with_classes:

                            paragraphs = div_with_classes.find_all('p')

                            filtered_paragraphs = []
                            for paragraph in paragraphs:

                                if not any(paragraph.find_parents(['b', 'a'])):
                                    filtered_paragraphs.append(paragraph)
                            text = ''
                            for paragraph in filtered_paragraphs:
                                text += paragraph.text
                            text = text.replace('\n', '')
                            text = re.sub(r'[,|\t]', ' ', text)
                            text = text.replace('\n', '')
                        else:
                            text = "No text found"
                        self.write_to_csv({
                            'title': title,
                            'url': link,
                            'text': text,
                            'category': 'Seguridad Informatica'
                        })

        except requests.exceptions.RequestException as e:
            logging.error(f"Error de solicitud HTTP: {e}")

        except ET.ParseError as e:
            logging.error(f"Error al analizar XML: {e}")

        except AttributeError as e:
            logging.error(f"Error de atributo: {e}")

    def scrape_cars_news(self):
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(self.cars_url, headers=headers, stream=True)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                url_list = []
                for url_elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
                    loc_elem = url_elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                    if loc_elem is not None:
                        url = loc_elem.text
                        url_list.append(url)
                for url in url_list[1:self.counts]:
                    headers = {'User-Agent': self.user_agent}
                    response_url = requests.get(url, headers=headers, stream=True)
                    if response_url.status_code == 200:
                        soup = BeautifulSoup(response_url.text, 'html.parser')
                        title = soup.h1.text
                        title = title.replace('\n', '').lstrip()
                        div_articule = soup.find('div', class_='prueba-content')
                        text = div_articule.text.replace('\n', '').lstrip()
                        self.write_to_csv({
                            'title': title,
                            'url': url,
                            'text': text,
                            'category': 'Autos'
                        })

        except Exception as e:
            logging.error(f"Error al obtener noticias de autos: {e}")

    def scrape_sports_news(self):
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(self.sports_url, headers=headers, stream=True)
            if response.status_code == 200:
                root = ET.fromstring(response.content)

                url_list = []
                for url_elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
                    loc_elem = url_elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                    if loc_elem is not None:
                        url = loc_elem.text
                        url_list.append(url)

                for url in url_list[1:self.counts]:
                    headers = {'User-Agent': self.user_agent}
                    response_url = requests.get(url, headers=headers, stream=True)
                    if response_url.status_code == 200:
                        soup = BeautifulSoup(response_url.text, 'html.parser')

                        div_with_classes = soup.find('div', class_='article-body')
                        if div_with_classes:
                            paragraphs = div_with_classes.find_all('p')
                            titulo = soup.h1.text
                            titulo = titulo.replace('\n', '').lstrip()
                            texto = ''
                            for paragraph in paragraphs:
                                texto += paragraph.text
                            texto = texto.replace('\n', '')
                            self.write_to_csv({
                                'title': titulo,
                                'url': url,
                                'text': texto,
                                'category': 'Deportes'
                            })
                        else:
                            logging.warning(f"Div with classes not found in {url}")
                    else:
                        logging.error(f"Failed to retrieve {url}. Status code: {response_url.status_code}")
        except Exception as e:
            logging.error(f"Error en la función de scraping de noticias de deportes: {e}")

    def scrape_food_news(self):
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(self.food_url, headers=headers, stream=True)
            if response.status_code == 200:
                root = ET.fromstring(response.content)

                url_list = []
                for url_elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
                    loc_elem = url_elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                    if loc_elem is not None:
                        url_list.append(loc_elem.text)

                for url in url_list[1:self.counts]:
                    headers = {'User-Agent': self.user_agent}
                    response_url = requests.get(url, headers=headers, stream=True)
                    if response_url.status_code == 200:
                        soup = BeautifulSoup(response_url.text, 'html.parser')

                        div_with_classes = soup.find('div', class_='container container--no-padding-md')
                        if div_with_classes:
                            paragraphs = div_with_classes.find_all('p')
                            titulo = soup.h1.text
                            titulo = titulo.replace('\n', '').lstrip()
                            texto = ''
                            for paragraph in paragraphs:
                                texto += paragraph.text
                            texto = texto.replace('\n', '')
                            self.write_to_csv({
                                'title': titulo,
                                'url': url,
                                'text': texto,
                                'category': 'Recetas'
                            })
                        else:
                            logging.warning(f"Div with classes not found in {url}")
                    else:
                        logging.error(f"Failed to retrieve {url}. Status code: {response_url.status_code}")
        except Exception as e:
            logging.error(f"Error en la función de scraping de noticias de comida: {e}")

    def run_scrapers(self):
        threads = [threading.Thread(target=self.scrape_security_news),
                   threading.Thread(target=self.scrape_cars_news),
                   threading.Thread(target=self.scrape_sports_news),
                   threading.Thread(target=self.scrape_food_news)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
