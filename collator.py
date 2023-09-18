import requests
import csv
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from dotenv import load_dotenv

# python -m venv project_venv         --creates virtual environment
# source project_venv/bin/activate    --activates virtual environment
# (project_venv) $deactivate          --deactivates virtual environment


def google_search(query):
    load_dotenv()
    api_key = os.getenv('API_KEY')

    url = "https://places.googleapis.com/v1/places:searchText"

    payload = {"textQuery": query}
    headers = {
        "Content-Type": "application/json",
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.websiteUri,places.nationalPhoneNumber,places.rating",
        "X-Goog-Api-Key": api_key
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    if response.status_code == 200:
        place_data = response.json()

        class Place:
            def __init__(self, name, address, number, rating, website):
                self.name = name
                self.address = address
                self.number = number
                self.rating = rating
                self.website = website

        place_objects = []

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


def perform_search():
    query = search_input.text()
    search_results = google_search(query)

    if search_results:
        status_label.setText("Search successful!")
        status_label.setStyleSheet("color: green;")
        csvExport(search_results)

    else:
        status_label.setText("Search failed!")
        status_label.setStyleSheet("color: red;")
        print('no results')


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Google Results Collator")

search_label = QLabel("Enter search query:")
search_input = QLineEdit()

status_label = QLabel("")
status_label.setAlignment(Qt.AlignCenter)

search_button = QPushButton("Search")
search_button.clicked.connect(perform_search)

layout = QVBoxLayout()
layout.addWidget(search_label)
layout.addWidget(search_input)
layout.addWidget(search_button) 
layout.addWidget(status_label)

window.setLayout(layout)

window.show()
sys.exit(app.exec_())
