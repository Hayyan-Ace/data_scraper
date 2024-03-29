import csv
from bs4 import BeautifulSoup
import requests

url = "https://www.politifact.com/"
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')

# List to store data for each post
posts_data = []

posts = soup.find_all('article', class_="m-statement")

for post in posts:
    # Dictionary to store data for the current post
    post_data = {}

    author_tag = post.find('a', class_="m-statement__name")
    if author_tag:
        author_name = author_tag.text.strip()
        post_data['Author'] = author_name

    quote = post.find('div', class_="m-statement__quote")
    if quote:
        quote_text = quote.text.strip()
        post_data['Quote'] = quote_text

    meter_div = post.find('div', class_='m-statement__body')
    if meter_div:
        footer = meter_div.find('footer', class_="m-statement__footer")
        if footer:
            footer_text = footer.text.strip()
            post_data['Footer'] = footer_text

        meter = meter_div.find('div', class_='m-statement__meter')
        if meter:
            img_tag = meter.find('img', class_='c-image__original')
            if img_tag and 'src' in img_tag.attrs:
                image_src = img_tag['src']
                post_data['Image Source'] = image_src

    # Append post data to the list
    posts_data.append(post_data)

# Write data to CSV file
filename = 'scrapped_politifact.csv'
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Author', 'Quote', 'Footer', 'Image Source']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for post_data in posts_data:
        writer.writerow(post_data)

print(f"Data has been written to {filename}")
