import os
from dotenv import load_dotenv
import requests
import json
from geo import get_geo

def get_nearby(text):
    load_dotenv()
    url = os.environ['URL_NEAR']
    headers ={
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': os.environ['API_KEY'], 
    'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.rating,places.currentOpeningHours'
    }
    lat = get_geo(text)[0]
    lng = get_geo(text)[1]

    data ={
        "includedTypes": ['hotel','hostel','motel','resort_hotel','lodging'],
        "maxResultCount": 2,
        "rankPreference": "DISTANCE",
        "locationRestriction": {
            'circle': {
                'center':{
                    'latitude': f'{lat}',
                    'longitude': f'{lng}'},
                'radius': 1000.0
            }
        } 
    }
    response = requests.post(url, json=data, headers=headers)
    response = response.text
    response = json.loads(response)
    return response


# # print(get_nearby(15213))
if __name__ == '__main__':
    print(get_nearby(15213))
