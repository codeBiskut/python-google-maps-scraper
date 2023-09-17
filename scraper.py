import requests
import json
import csv

# python -m venv project_venv         --creates virtual environment
# source project_venv/bin/activate    --activates virtual environment
# (project_venv) $deactivate          --deactivates virtual environment


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
            name = place.get('displayName.text')
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

def main():
    search_query = 'kayaks near me'
    search_results = google_search(search_query)

    if search_results:
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