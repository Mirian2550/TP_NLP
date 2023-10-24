from clasificador.clasificador import SVMClassifier
from scrapper.scrapper import Scraper

output_file = 'data/dataset.csv'
security_url = 'https://blog.segu-info.com.ar/sitemap.xml'
technology_url = 'url2'
sports_url = 'url3'
food_url = 'https://www.recetasnestle.com.mx/sitemap.xml'

scraper = Scraper(output_file, security_url, technology_url, sports_url, food_url)
scraper.run_scrapers()

svm_classifier = SVMClassifier(output_file, kernel='linear', C=1.0)
svm_classifier.train()

accuracy = svm_classifier.evaluate()
print(f'Precisión del modelo SVM: {accuracy}')