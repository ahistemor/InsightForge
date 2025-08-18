from bs4 import BeautifulSoup
import requests
import time 
import pandas as pd
import re

# uala has 3 sites: mexico, argentina, colombia. Each site has his own sites

def obtainUalaNewsLinks (link):
    url = requests.get(link).text
    
    page = BeautifulSoup(url, 'html.parser')
    
    site_sections = page.find_all('div', {'class' : 'c-bqDmIL c-bqDmIL-ewJRzd-columns-3'})
    
    list_links = []
    
    res = re.findall('.co/|.ar/|.mx/', link)
    
    if res[0] == '.mx/':
        country_site = 'https://www.uala'
    else:
        country_site = 'https://www.uala.com'        
    
    for section in site_sections:
        news_links = section.find_all('article')
        
        for link in news_links:
            
            if res[0] == '.mx/':
                temp_link = link.find_all('a')[0].get("href").replace(' ', '%20')
            else:
                temp_link = link.find_all('a')[0].get("href")
                
            list_links.append(country_site + res[0].replace('/','') + temp_link)
    
    return list_links


list_links = obtainUalaNewsLinks('https://www.uala.com.ar/anuncios')

list_links = obtainUalaNewsLinks('https://www.uala.com.co/prensa')

list_links = obtainUalaNewsLinks('https://www.uala.mx/anuncios')
 
#####################################

titles = []
dates = []
summaries = []
paragraphs = []

i = 1

for link in list_links:
    url = requests.get(link).text
    page = BeautifulSoup(url, 'html.parser')    
  
    titles.append(page.find_all('h1')[0].text.strip())
    
    paragraph = page.find_all('p')    

    if not paragraph[0].find_all('strong'):
        paragraph = paragraph[1]
    else:
        paragraph = paragraph[0]
    
    paragraphs.append(paragraph.text.strip())
    
    if not paragraph.find_all('strong'):
        dates.append('')
    else:
        dates.append(paragraph.find_all('strong')[0].text.strip())        

    if not page.find_all('h3'):
        summaries.append('')
    elif len(page.find_all('h3')) > 1:
        summaries.append(page.find_all('h3')[0].text.strip() + ' ' + (page.find_all('h3')[1].text.strip()))
    else:
        summaries.append(page.find_all('h3')[0].text.strip())       

    print(f"    Progress: {str(round((i/len(list_links))*100,0)) + '%'}", end="\r", flush=True)
    i += 1


df = pd.DataFrame({
    'link': list_links,
    'title': titles,
    'date': dates,
    'summary': summaries,
    'paragraph': paragraphs
})

df.to_csv('data/uala_news.csv', index=False, encoding='utf-8')
