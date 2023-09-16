import requests
from bs4 import BeautifulSoup

# $ python -m venv project_venv     --creates virtual environment
# $ source project_venv/bin/activate    --activates virtual environment
# (project_venv) $ deactivate       --deactivates virtual environment


def google_search(query):
    base_url = 'https://www.google.com/search'
    params = {
        'q': query,
        'hl': 'en' # set the language to return
    }

    headers = {
        'User-Agent': 'MoziMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(base_url, params=params,headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        for item in soup.select('.tF2Cxc'):
            title = item.h3.get_text()
            link = item.a['href']
            snippet = item.select_one('.aCOpRe').get_text()
            results.append({'title': title, 'link': link, 'snippet': snippet})

        return results

    else:
        print('Error:', response.status_code)
        return None

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

if __name__ == '__main__':
    main()