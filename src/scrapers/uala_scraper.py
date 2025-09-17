from bs4 import BeautifulSoup
import requests
import time 
import pandas as pd
import re
from src.utils import UalaScraper


# uala has 3 sites: mexico, argentina, colombia. Each site has his own sites
df_ar = UalaScraper.UalaScraper('ar').scrape_news()
df_co = UalaScraper.UalaScraper('co').scrape_news()
df_mex = UalaScraper.UalaScraper('mx').scrape_news()

df_uala = pd.concat([df_ar, df_co, df_mex])

UalaScraper.UalaScraper.save_to_csv(df_uala, 'data/uala_news.csv')

