import requests
import json
import csv

# $ python -m venv project_venv     --creates virtual environment
# $ source project_venv/bin/activate    --activates virtual environment
# (project_venv) $ deactivate       --deactivates virtual environment


def google_search(query):
    url = "https://places.googleapis.com/v1/places:searchText"

    payload = {"textQuery": "kayaks near me"}
    headers = {
        "Content-Type": "application/json",
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.websiteUri,places.nationalPhoneNumber,places.rating",
        "X-Goog-Api-Key": "AIzaSyD2m5kAcnJsPseSkz2CKlZcOF5ijIhQSIM"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    if response.status_code == 200:
        

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

    # else:
    #     print('no results')

if __name__ == '__main__':
    main()