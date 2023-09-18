import requests
import csv
import os
from dotenv import load_dotenv

# python -m venv project_venv         --creates virtual environment
# source project_venv/bin/activate    --activates virtual environment
# (project_venv) $deactivate          --deactivates virtual environment


def google_search(query):
    load_dotenv()
    api_key = os.getenv('API_KEY')

    url = "https://places.googleapis.com/v1/places:searchText"

    payload = {"textQuery": "breweries near me"}
    headers = {
        "Content-Type": "application/json",
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.websiteUri,places.nationalPhoneNumber,places.rating",
        "X-Goog-Api-Key": api_key
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    if response.status_code == 200:
        #parse json response into list of dictionaries
        place_data = response.json()

        #class for objects
        class Place:
            def __init__(self, name, address, number, rating, website):
                self.name = name
                self.address = address
                self.number = number
                self.rating = rating
                self.website = website

        #list of places
        place_objects = []

        #iterate through dictionary lists and create objects
        for place in place_data.get("places", []):
            name = place.get('displayName', {}).get('text')
            address = place.get('formattedAddress')
            number = place.get('nationalPhoneNumber')
            rating = place.get('rating')
            website = place.get('websiteUri')
            place = Place(name, address, number, rating, website)
            place_objects.append(place)

        return place_objects

    else:
        print('Error:', response.status_code)
        return None
    
def csvExport(search_results):
    list_of_dicts = []
    for place in search_results:
        place_dict = {
            "name": place.name,
            "address": place.address,
            "number": place.number,
            "rating": place.rating,
            "website": place.website
        }
        list_of_dicts.append(place_dict)

    #need to ask for filename
    csv_file_name = 'output.csv'

    csv_header = list_of_dicts[0].keys() if search_results else []

    with open(csv_file_name, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_header)
        writer.writeheader()
        writer.writerows(list_of_dicts)

    print(f'CSV data has been written to {csv_file_name}')


def main():
    search_query = 'breweries'
    search_results = google_search(search_query)

    if search_results:
        csvExport(search_results)
        for result in search_results:
            print(f"Name: {result.name}")
            print(f"Address: {result.address}")
            print(f"Number: {result.number}")
            print(f"Rating: {result.rating}")
            print(f"Website: {result.website}")
            print('\n')

    else:
        print('no results')

if __name__ == '__main__':
    main()