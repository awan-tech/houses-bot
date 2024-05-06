import os
from pathlib import Path
import slack
import requests
import json
from dotenv import load_dotenv
from flask import Flask, request, Response
from geo import get_geo
from PIL import Image
from io import BytesIO
from nearby import get_nearby


def get_map(text):
    load_dotenv()
    CENTER = str(get_geo(text)[0])+','+str(get_geo(text)[1])
    ZOOM = 15
    SIZE = '700x700'
    API_KEY = os.environ['API_KEY_MAP']
    MAP_TYPE = 'roadmap'
    nb_response = get_nearby(text)
    try:
        MARKERS = f'&markers=size:mid%7Clabel:U%7Ccolor:blue%7C{CENTER}'
        for i in nb_response['places']:
            AD = i.get('formattedAddress','No data')
            AD = str(AD).replace(' ','')
            MARKERS=MARKERS+f'&markers=size:mid%7Clabel:S%7Ccolor:red%7C{AD}'
        url_route = 'https://maps.googleapis.com/maps/api/staticmap?'
        url_query = f'center={CENTER}' + f'&zoom={ZOOM}' + f'&size={SIZE}' + f'&maptype={MAP_TYPE}' + MARKERS + f'&key={API_KEY}'
        URL = url_route+url_query
        response = requests.get(URL)
        image = Image.open(BytesIO(response.content))
        # image.show()
        return response.content
    except:
        return None

if __name__ == '__main__':
    print(get_map(15213))