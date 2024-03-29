import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_html(url):              #ping and extract link
    response = requests.get(url)
    return response.text

def extract_data(html):
    soup = BeautifulSoup(html, 'html.parser')       #parsing
    img_sources = [img['src'] for img in soup.find_all('img', src=True)]
    videos = [video['src'] for video in soup.find_all('video', src=True)]
    links = [link['href'] for link in soup.find_all('a', href=True)]
    texts = []
    for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span','div']:
        texts.extend([text.get_text() for text in soup.find_all(tag)])
    return img_sources, videos, links, texts

def save_to_csv(data, filename):    # saving data according to the dataframes
    df = pd.DataFrame(data, columns=['Value'])
    df.to_csv(filename, index=True)
    print(f"Data saved to {filename}")

def scrape_and_save(url):   #function call that calls multiple functions
    html = get_html(url)
    img_sources, videos, links, texts = extract_data(html)
    save_to_csv(img_sources, 'image_data.csv')
    save_to_csv(videos, 'video_data.csv')
    save_to_csv(links, 'link_data.csv')
    save_to_csv(texts, 'text_data.csv')

if __name__ == "__main__":
    url = 'https://www.altnews.in'
    scrape_and_save(url)