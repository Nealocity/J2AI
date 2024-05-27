import feedparser
import requests
from concurrent.futures import ThreadPoolExecutor

# Function to extract content from a link and write to a file
def extract_content(link):
    try:
        print(f'{link}')
        response = requests.get(link)
        content = response.text
        #print(f'{content}')   
        print(f'{output_text_file}') 

        with open(output_text_file, "a") as file:
            file.write(content + "\n\n")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {link}: {e}")

# Function to load and parse the RSS feed
def load_rss_and_extract_content(rss_url):
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)
    #print(f'{feed}')
    # List to hold all the links
    links = [entry.link for entry in feed.entries]
    print(f'{links}')

    
    # Use ThreadPoolExecutor to execute reading from multiple links in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(extract_content, links)

# Replace 'your_rss_feed_url.xml' with your actual RSS feed URL
rss_url = 'D:\content\source\RSS_feed.xml'
output_text_file = 'D:/content/source/RSS_output.txt'
load_rss_and_extract_content(rss_url)