import csv
import multiprocessing
import random
import re

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import logging


def remove_p_with_a(tag):
    return tag.name == 'p' and tag.find('a')


def remove_p_with_span(tag):
    return tag.name == 'p' and tag.find('span')


def clean_p(div_with_classes):
    noscript_elements = div_with_classes.find_all('noscript')
    for noscript in noscript_elements:
        noscript.extract()
    img_elemnts = div_with_classes.find_all('img')
    for img in img_elemnts:
        img.extract()
    script_elements = div_with_classes.find_all('script')
    for script in script_elements:
        script.extract()

    div_elements = div_with_classes.find_all('div')
    for div in div_elements:
        div.extract()
    section_elements = div_with_classes.find_all('section')
    for div in section_elements:
        div.extract()

    span_elements = div_with_classes.find_all('span')
    for div in span_elements:
        div.extract()
    p_elements_with_a = div_with_classes.find_all(remove_p_with_a)
    for p in p_elements_with_a:
        p.extract()

    p_elements_with_span = div_with_classes.find_all(remove_p_with_span)
    for p in p_elements_with_span:
        p.extract()

    paragraphs = div_with_classes.find_all('p')
    text = ''
    for paragraph in paragraphs:
        text += paragraph.text
    text = text.replace('\n', '')
    text = re.sub(r'[,|\t]', ' ', text)
    text = text.replace('\n', '')
    return text


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
    def __init__(self, output_file, security_url, baby_url, sports_url, food_url, counts=50, request_delay=1):
        """
        constructor de la clase Scraper con las URLs de los sitios a trabajar.

        Args:
            request_delay: tiempo entre peticion
            output_file (str): Nombre del archivo CSV de salida.
            security_url (str): URL de noticias de seguridad .xml.
            baby_url (str): URL de noticias de bendis.
            sports_url (str): URL de noticias de deportes.
            food_url (str): URL de noticias de comida .
            counts (int): Número de noticias a raspar.
        """
        self.security_url = security_url
        self.baby_url = baby_url
        self.sports_url = sports_url
        self.food_url = food_url
        self.output_file = output_file
        self.counts = counts
        self.user_agent = get_random_user_agent()
        self.request_delay = request_delay

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
                fieldnames = ['title', 'url', 'text', 'category']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')

                if csvfile.tell() == 0:
                    writer.writeheader()

                records = []
                text_cleaned = data['text'].strip().replace(',', '').replace('.', '').replace(';', '')
                text_cleaned = text_cleaned.replace('"', '')
                records.append({
                    'title': data['title'].lower(),
                    'url': data['url'],
                    'text': text_cleaned.lower(),
                    'category': data['category']
                })

                writer.writerows(records)
        except Exception as e:
            logging.error(f"Error al escribir en el archivo CSV: {e}")

    def get_news_urls(self, url):
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, stream=True)
            url_max = self.counts
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                url_list = []
                for url_elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
                    loc_elem = url_elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
                    if loc_elem is not None and (len(url_list) < url_max):
                        url = loc_elem.text
                        url_list.append(url)
                return url_list
        except Exception as e:
            logging.error(f"Error al obtener URLs de noticias: {e}")
            return []

    def scrape_url(self, url, body='entry-content clear', category='Bebes'):
        try:
            headers = {'User-Agent': self.user_agent}
            response_url = requests.get(url, headers=headers, stream=True)
            if response_url.status_code == 200:
                soup = BeautifulSoup(response_url.text, 'html.parser')

                if category == 'Seguridad Informatica':
                    title = soup.find('h2', class_='post-title entry-title')
                    if title:
                        title = title.text.replace('\n', '').lstrip()
                    else:
                        title = "No title found"
                else:
                    title = soup.h1.text
                    title = title.replace('\n', '').lstrip()
                div_with_classes = soup.find('div', class_=body)
                if div_with_classes:
                    text = clean_p(div_with_classes)
                    self.write_to_csv({
                        'title': title,
                        'url': url,
                        'text': text,
                        'category': category
                    })
        except Exception as e:
            logging.error(f"Error al obtener noticias : {e}")

    def scrape_security_news(self):
        security_news_urls = self.get_news_urls(self.security_url)
        processes = [
            multiprocessing.Process(
                target=self.scrape_url, args=(url, 'post-body entry-content', 'Seguridad Informatica')) for url in
            security_news_urls
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join()

    def scrape_baby_news(self):
        baby_news_urls = self.get_news_urls(self.baby_url)
        processes = [
            multiprocessing.Process(target=self.scrape_url, args=(url, 'entry-content clear', 'Bebes')) for url in
            baby_news_urls
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join()

    def scrape_sports_news(self):
        sports_news_urls = self.get_news_urls(self.sports_url)
        processes = [
            multiprocessing.Process(target=self.scrape_url, args=(url, 'article-body', 'Deportes')) for url in
            sports_news_urls
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join()

    def scrape_food_news(self):
        food_news_urls = self.get_news_urls(self.food_url)
        processes = [
            multiprocessing.Process(
                target=self.scrape_url, args=(url, 'container container--no-padding-md', 'Recetas')) for url in
            food_news_urls
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join()

    def run_scrapers(self):
        processes = [
            multiprocessing.Process(target=self.scrape_security_news),
            multiprocessing.Process(target=self.scrape_baby_news),
            multiprocessing.Process(target=self.scrape_sports_news),
            multiprocessing.Process(target=self.scrape_food_news)
        ]

        for process in processes:
            process.start()

        for process in processes:
            process.join()



