import os
from dotenv import load_dotenv
import requests
import json

def get_detail(text):
    load_dotenv()
    url = os.environ['URL_TEXT']
    headers ={
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': os.environ['API_KEY'],
    'X-Goog-FieldMask': 'places.displayName,places.location,places.plusCode,places.formattedAddress'
    }
    data = {
        'textQuery': text
    }
    response = requests.post(url, json=data, headers=headers)
    response = response.text
    return response


if __name__ == '__main__':
    print('This is a module')