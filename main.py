from scrapper.scrapper import Scraper

output_file = 'data/dataset.csv'
security_url = 'url1'
technology_url = 'url2'
sports_url = 'url3'
food_url = 'url4'

scraper = Scraper(output_file, security_url, technology_url, sports_url, food_url)
scraper.run_scrapers()
