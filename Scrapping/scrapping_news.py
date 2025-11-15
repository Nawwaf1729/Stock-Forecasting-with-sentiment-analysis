pip install beautifulsoup4

#Importing Library
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from datetime import datetime

#Web Access Checking
# Send a GET request to the specified URL
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get('https://www.investing.com', headers=HEADERS, timeout=15)

# Check if the request was successful (status code 200)
if response.status_code == 200:
  html_content = response.content
  print(html_content)
else:
	print(response)

# Parse HTML

soup = BeautifulSoup(response.text, 'html.parser')

# HTML Structure

print(soup.prettify())

#Detail News Access Checking
# Send a GET request to the specified URL
response_news = requests.get('https://finansial.bisnis.com/read/20251012/90/1919508/investor-asing-lepas-saham-perbankan-bbri-dan-bbca-dilego-triliunan?utm_source=desktop&utm_medium=search', headers=HEADERS)

# Check if the request was successful (status code 200)
if response_news.status_code == 200:
  html_content = response_news.content
  print(html_content)
else:
  print(response_news)

# Parse HTML

soup_news = BeautifulSoup(response_news.text, 'html.parser')

# Extract Article paragraphs within the artContent div
article = '' # Initialize article as an empty string
article_content_div = soup_news.find('article', class_='detailsContent force-17 mt40')
if article_content_div:
    paragraphs = article_content_div.find_all('p')
    for p in paragraphs:
        article += p.get_text() + "\n"

print(article_content_div)

# --- CONFIGURATION ---
KEYWORD = "BBRI"
START_DATE = "2023/10/09"
TO_DATE = "2025/10/07"
START_PAGE = 1
END_PAGE = 251

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_article_details(article_url):
    """
    Function to retrieve details (title, date, url) from a single CNBC article URL.
    """
    try:
        time.sleep(1)
        page = requests.get(article_url, headers=HEADERS, timeout=20)

        if page.status_code != 200:
            print(f"  Failed to retrieve: {article_url}, Status: {page.status_code}")
            return None

        soup = BeautifulSoup(page.text, 'html.parser')

        # --- Data Extraction From Detail Page ---

        title = 'Title Not Found'
        publish_date = 'Date Not Found'
        article = ' '

        scripts = soup.find_all('script', type='text/javascript')
        for script in scripts:
            if script.string and 'dataLayer' in script.string:
                # Title Extraction
                title_match = re.search(r"'originalTitle'\s*:\s*'([^']*)'", script.string)
                if title_match:
                    title = title_match.group(1)

                # Date Extraction
                date_match = re.search(r"'publishDate'\s*:\s*'([^']*)'", script.string)
                if date_match:
                    publish_date = date_match.group(1)

                # If both are found, stop the loop
                if title != 'Title not found' and publish_date != 'Date Not Found':
                    break

        paragraphs = soup.find_all('p')
        for p in paragraphs:
            article += p.get_text() + "\n"
            article = article.replace('\n', ' ')

        return {
            'Publish_date': publish_date,
            'URL': article_url,
            'Title': title,
            'Article': article
        }

    except Exception as e:
        print(f"  Error when processing {article_url}: {e}")
        return None

if __name__ == "__main__":
    list_article = []

    for page_num in range(START_PAGE, END_PAGE + 1):
        search_url = f"https://www.cnbcindonesia.com/search?query={KEYWORD}&fromdate={START_DATE}&todate={TO_DATE}&tipe=artikel&page={page_num}"

        print(f"--- Retrieving data from page #{page_num} ---")

        try:
            main_page = requests.get(search_url, headers=HEADERS, timeout=15)

            if main_page.status_code == 200:
                soup = BeautifulSoup(main_page.text, 'html.parser')

                article_links = soup.select('article a.group')

                if not article_links:
                    print("No more articles were found on this page.")
                    break

                for link_tag in article_links:
                    if link_tag.has_attr('href'):
                        article_url = link_tag['href']
                        print(f"  Found an article: {article_url}")

                        article_data = get_article_details(article_url)

                        if article_data:
                            list_article.append(article_data)

                print(f"Retrieved data from page {page_num}.")
                time.sleep(3)
            else:
                print(f"Failed to retrieve page {page_num}, Status: {main_page.status_code}")

        except Exception as e:
            print(f"Error when retrieve page {page_num}: {e}")

    df = pd.DataFrame(list_article)
    print("\n--- DATAFRAME RESULT ---")
    print(df)
    print("\n--- FINISH ---")
    df.to_csv('BBRI_Sentiment_CNBC.csv', index=False)

# --- CONFIGURATION ---
KEYWORD = "BBRI"
START_PAGE = 1
END_PAGE = 54

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_article_details(article_url):
    """
    Function to retrieve details (title, date, url, summary, article) from a single news article URL.
    """
    try:
        time.sleep(1)
        page = requests.get(article_url, headers=HEADERS, timeout=20)

        if page.status_code != 200:
            print(f"  Failed to retrieve: {article_url}, Status: {page.status_code}")
            return None

        soup = BeautifulSoup(page.text, 'html.parser')

        # --- Data Extraction From Detail Page ---

        title = 'Title Not Found'
        publish_date = 'Date Not Found'
        article = ' '

        # Extract Title from meta tag
        title_meta = soup.find('meta', property='og:title')
        if title_meta and title_meta.get('content'):
            title = title_meta['content']

        # Extract Publish Date from meta tag
        date_meta = soup.find('meta', property='article:published_time')
        if date_meta and date_meta.get('content'):
            datetime_string = date_meta['content']
            try:
              match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', datetime_string)
              if match:
                datetime_obj = datetime.fromisoformat(match.group(1))
                # Format the datetime object to show only date and time
                publish_date = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
              else:
                print(f"Could not parse datetime string format: {datetime_string}")
            except ValueError as e:
              print(f"Error parsing datetime string: {e}")

        # Extract Article paragraphs within the artContent div
        article_content_div = soup.find('article', class_='detailsContent force-17 mt40')
        if article_content_div:
            paragraphs = article_content_div.find_all('p')
            for p in paragraphs:
                article += p.get_text() + "\n"

            article = article.replace('\n', ' ')

        return {
            'Publish_date': publish_date,
            'URL': article_url,
            'Title': title,
            'Article': article
        }

    except Exception as e:
        print(f"  Error when processing {article_url}: {e}")
        return None

if __name__ == "__main__":
    list_article = []
    processed_urls = set() # Use a set to store processed URLs

    for page_num in range(START_PAGE, END_PAGE + 1):
        search_url = f"https://search.bisnis.com/?q={KEYWORD}&page={page_num}"

        print(f"--- Retrieving data from page #{page_num} ---")

        try:
            main_page = requests.get(search_url, headers=HEADERS, timeout=15)

            if main_page.status_code == 200:
                soup = BeautifulSoup(main_page.text, 'html.parser')

                # Find all article links on the search results page
                article_links = soup.select('a.artLink')

                if not article_links:
                    print("No more articles were found on this page.")
                    break

                for link_tag in article_links:
                    if link_tag.has_attr('href'):
                        article_url = link_tag['href']

                        # Clean up the URL if it's a search redirect link
                        if "search.bisnis.com/link?url=" in article_url:
                            from urllib.parse import unquote
                            cleaned_url = unquote(article_url.split("url=")[-1])
                            article_url = cleaned_url

                        # Check if the URL has already been processed
                        if article_url not in processed_urls:
                            print(f"  Found an article: {article_url}")
                            article_data = get_article_details(article_url)

                            if article_data:
                                list_article.append(article_data)
                                processed_urls.add(article_url) # Add the processed URL to the set
                        else:
                            print(f"  Skipping duplicate article: {article_url}")


                print(f"Retrieved data from page {page_num}.")
                time.sleep(3)
            else:
                print(f"Failed to retrieve page {page_num}, Status: {main_page.status_code}")

        except Exception as e:
            print(f"Error when retrieve page {page_num}: {e}")

    df = pd.DataFrame(list_article)
    print("\n--- DATAFRAME RESULT ---")
    print(df)
    print(df.info())
    print("\n--- FINISH ---")
    df.to_csv('BBRI_Sentiment_Bisnis.csv', index=False)

