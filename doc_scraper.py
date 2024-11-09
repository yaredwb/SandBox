import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time
import random

def fetch_page(url):
    headers = {
        'User-Agent': 'CrewaiScraper/1.0 (+https://yourdomain.com/info)'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def is_valid_url(url, base_url):
    parsed_base = urlparse(base_url)
    parsed_url = urlparse(url)
    return parsed_url.netloc == parsed_base.netloc and parsed_url.scheme in ['http', 'https']

def extract_content(soup):
    content = {}
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for header in headers:
        header_text = header.get_text(strip=True)
        content[header_text] = []
        sibling = header.find_next_sibling()
        while sibling and sibling.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if sibling.name == 'p':
                content[header_text].append(sibling.get_text(strip=True))
            sibling = sibling.find_next_sibling()
    return content

def crawl_site(start_url):
    to_visit = [start_url]
    visited = set()
    site_data = {}

    while to_visit:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue
        print(f"Scraping: {current_url}")
        try:
            html = fetch_page(current_url)
            soup = BeautifulSoup(html, 'html.parser')
            
            content = extract_content(soup)
            site_data[current_url] = content

            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                full_url = urljoin(current_url, href)
                if is_valid_url(full_url, start_url) and full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)
            
            # Implement delay to respect server
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Failed to scrape {current_url}: {e}")
        finally:
            visited.add(current_url)
    
    return site_data

def save_data_to_json(data, filename='crewai_docs.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    start_url = "https://docs.crewai.com/introduction"
    scraped_data = crawl_site(start_url)
    save_data_to_json(scraped_data)
    print("Scraping completed and data saved to crewai_docs.json")
