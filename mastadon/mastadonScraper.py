import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time


# Function to scrape a single page
def scrape_page(driver, aria_label_map):
    # Get the HTML content of the page
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Extract individual posts
    articles = soup.find_all('article')
    for article in articles:
        # Find the div with the class 'status__wrapper' within each article
        status_wrapper = article.find('div', class_='status__wrapper')
        if status_wrapper:
            # Extract the aria-label attribute
            aria_label = status_wrapper.get('aria-label')
            if aria_label and aria_label not in aria_label_map:
                thumbnail_hrefs = []
                # Find all <a> tags with class "media-gallery__item-thumbnail"
                thumbnails = status_wrapper.find_all('a', class_='media-gallery__item-thumbnail', href=True)
                for thumbnail in thumbnails:
                    thumbnail_href = thumbnail['href']
                    thumbnail_hrefs.append(thumbnail_href)

                link_hrefs = []
                links_posts = status_wrapper.find_all('a', class_='status-card', href=True)
                for link in links_posts:
                    link_href = link['href']
                    link_hrefs.append(link_href)

                # Store thumbnail and link hrefs against aria-label in the map
                aria_label_map[aria_label] = {'thumbnail_hrefs': thumbnail_hrefs, 'link_hrefs': link_hrefs}

                print("Aria Label:", aria_label)
                print("Thumbnail Hrefs:", thumbnail_hrefs)
                print("Link Hrefs:", link_hrefs)


# Function to scroll down by a specified amount
def scroll_down(driver, pixels):
    driver.execute_script(f"window.scrollBy(0, {pixels});")


# Function to scrape multiple pages
def scrape_multiple_pages(base_url, num_pages):
    driver = webdriver.Chrome()  # You need to have ChromeDriver installed
    driver.get(base_url)
    aria_label_map = {}  # Initialize an empty dictionary to store aria-labels and thumbnail hrefs

    for _ in range(num_pages):
        scrape_page(driver, aria_label_map)
        # Scroll down by 1000 pixels each time
        scroll_down(driver, 550)
        time.sleep(1)  # Wait for the new content to load

    driver.quit()
    return aria_label_map


# Function to write data to a CSV file
def write_to_csv(aria_label_map, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['aria_label', 'thumbnail_hrefs', 'link_hrefs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for aria_label, hrefs in aria_label_map.items():
            thumbnail_hrefs = ','.join(hrefs['thumbnail_hrefs'])
            link_hrefs = ','.join(hrefs['link_hrefs'])
            writer.writerow({'aria_label': aria_label, 'thumbnail_hrefs': thumbnail_hrefs, 'link_hrefs': link_hrefs})
    print(f"Data has been written to {filename}")


base_url = 'https://mastodon.social/explore'
num_pages_to_scrape = 1000
aria_label_map = scrape_multiple_pages(base_url, num_pages_to_scrape)

filename = 'scraped_data_by_hayyan.csv'
write_to_csv(aria_label_map, filename)
