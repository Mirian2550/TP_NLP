import threading

import requests
import csv
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, output_file, security_url, technology_url, sports_url, food_url, counts=10):
        self.security_url = security_url
        self.technology_url = technology_url
        self.sports_url = sports_url
        self.food_url = food_url
        self.output_file = output_file
        self.counts = counts

    def write_to_csv(self, data):
        with open(self.output_file, 'w', newline='') as csvfile:
            fieldnames = ['title', 'url', 'text']  # Estructura del CSV: título, URL, texto
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for item in data:
                writer.writerow({
                    'title': item['title'],
                    'url': item['url'],
                    'text': item['text']
                })

    def scrape_security_news(self):
        pass

    def scrape_technology_news(self):
        pass

    def scrape_sports_news(self):
        pass

    def scrape_food_news(self):
        pass

    def run_scrapers(self):
        threads = []
        threads.append(threading.Thread(target=self.scrape_security_news))
        threads.append(threading.Thread(target=self.scrape_technology_news))
        threads.append(threading.Thread(target=self.scrape_sports_news))
        threads.append(threading.Thread(target=self.scrape_food_news))
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
