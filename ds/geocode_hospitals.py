import json
import os
from pathlib import Path
import time

import requests
import pandas as pd


# Read Google Maps API key from the environment.
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']


def geocode(address):

    # Replace blanks with "+" as required by the API.
    address = address.replace(' ', '+')

    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}'
    print(url)
    response = requests.get(url)

    return json.loads(response.text)


def main():

    # Read raw hospitals dataset with name and address.
    input_filename = '../data/hospitals_raw.csv'
    hospitals = pd.read_csv(input_filename)

    # Are there duplicate hospitals?
    print('Total hospitals: {total}. Unique hospitals: {unique}'.format(total=hospitals.shape[0], unique=hospitals['Hospital name'].drop_duplicates().shape[0]))

    directory = '../data/locations'
    os.makedirs(directory, exist_ok=True)

    hospital_locations = []
    for i, hospital in hospitals.iterrows():

        # Get the name and address of the hospital.
        category = hospital['Category']
        hospital_name = hospital['Hospital name']
        hospital_address = hospital['Hospital address']

        # Address to geocode has both the name and address of the hospital.
        address = f'{hospital_name} {hospital_address}'

        # Do not download if we have already downloaded.
        path = Path(directory, f'{hospital_name}.json')
        if not os.path.exists(path):

            # Geocode the address to get lat/lng in a JSON.
            print(i, path)
            location = geocode(address)

            # Write the JSON for processing.
            with open(path, 'w') as f:
                json.dump(location, f, indent=4)

            # Delay before making the next request.
            time.sleep(1)
        else:
            with open(path) as f:
                location = json.load(f)

        geometry = location['results'][0]['geometry']['location']

        hospital_locations.append({
            'Category': category,
            'Hospital name': hospital_name,
            'Hospital address': hospital_address,
            'Hospital latitude': round(geometry['lat'], 6),
            'Hospital longitude': round(geometry['lng'], 6),
        })

    output_filename = '../data/hospital_locations.csv'
    hospital_locations = pd.DataFrame(hospital_locations).sort_values(by='Hospital name')
    hospital_locations[['Category', 'Hospital name', 'Hospital address', 'Hospital latitude', 'Hospital longitude']].to_csv(output_filename, index=False)


if __name__ == '__main__':
    main()
