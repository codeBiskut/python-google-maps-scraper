import requests
from bs4 import BeautifulSoup

def google_search(query):
    base_url = 'https://www.google.com/maps/search/'
    

def main():
    search_query = 'kayaks near me'
    search_results = google_search(search_query)

    if search_results:
        for i, result in enumerate(search_results, start=1):
            print(f"Result #{i}:")
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}")
            print('\n')

if __name__ == "__main__":
    main()