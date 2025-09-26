from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

class UalaScraper:
    COUNTRY_URLS = {
        'ar': 'https://www.uala.com.ar/anuncios',
        'co': 'https://www.uala.com.co/prensa',
        'mx': 'https://www.uala.mx/anuncios'
    }

    def __init__(self, country):
        if country not in self.COUNTRY_URLS:
            raise ValueError("Country must be one of: 'ar', 'co', 'mx'")
        self.country = country
        self.base_url = self.COUNTRY_URLS[country]
        self.links = []

    def obtain_news_links(self):
        url = requests.get(self.base_url).text
        page = BeautifulSoup(url, 'html.parser')
        site_sections = page.find_all('div', {'class': 'c-bqDmIL c-bqDmIL-ewJRzd-columns-3'})
        res = f".{self.country}/"
        country_site = 'https://www.uala' if self.country == 'mx' else 'https://www.uala.com'
        for section in site_sections:
            news_links = section.find_all('article')
            for link in news_links:
                temp_link = link.find_all('a')[0].get("href")
                if self.country == 'mx':
                    temp_link = temp_link.replace(' ', '%20')
                self.links.append(country_site + res.replace('/', '') + temp_link)

    def scrape_news(self):
        self.obtain_news_links()
        titles, dates, summaries, paragraphs, valid_links = [], [], [], [], []
        for i, link in enumerate(self.links, 1):
            try:
                url = requests.get(link)
                url.raise_for_status()  # Raises HTTPError for bad responses
                page = BeautifulSoup(url.text, 'html.parser')
            except Exception as e:
                print(f"Error fetching {link}: {e}")
                continue  # Skip to next link
            
            valid_links.append(link)
            h1_tags =  page.find_all('h1')
            if not h1_tags: 
                titles.append('')
            else:
                titles.append(h1_tags[0].text.strip())
            h3_tags = page.find_all('h3')
            if not h3_tags:
                if self.country == 'mx':
                    h4_tags = page.find_all('h4')
                    if not h4_tags:
                        ul_tags = page.find_all('li')
                        if not ul_tags:
                            summaries.append('')
                        else:
                          ul_tags_all = ul_tags[0].text.strip() + ' ' + ul_tags[1].text.strip()
                          summaries.append(ul_tags_all)
                    else:
                          summaries.append(h4_tags[0].text.strip())
                else:
                    summaries.append('')
            elif len(h3_tags) > 1:
                summaries.append(h3_tags[0].text.strip() + ' ' + h3_tags[1].text.strip())
            else:
                summaries.append(h3_tags[0].text.strip())
            paragraph_tags = page.find_all('p')
            if self.country == 'co':
                dates.append(paragraph_tags[0].find_all('strong')[0].text.strip())
                paragraphs.append(paragraph_tags[1].text.strip())
            else:
                paragraph = paragraph_tags[1] if not paragraph_tags[0].find_all('strong') else paragraph_tags[0]
                paragraphs.append(paragraph.text.strip())
                if not paragraph.find_all('strong'):
                    if self.country == 'mx':
                        dates.append(paragraph_tags[0].text.strip())
                    else:
                         dates.append('')
                else:
                    dates.append(paragraph.find_all('strong')[0].text.strip())
            print(f"    Progress: {str(round((i/len(self.links))*100,0)) + '%'}", end="\r", flush=True)

        return pd.DataFrame({
            'link': valid_links,
            'title': titles,
            'date': dates,
            'summary': summaries,
            'paragraph': paragraphs
        })

    def save_to_csv(df, filename):
        #df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')



