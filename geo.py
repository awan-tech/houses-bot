'''This script is used to get LAT and LNG of an address'''
import os
import googlemaps
from dotenv import load_dotenv

def get_geo(text):
    '''Get latitude and longtitude'''
    load_dotenv()
    gmaps = googlemaps.Client(key=os.environ['API_KEY'])
    geocode_result = gmaps.geocode(text)
    try:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return lat, lng
    except:
        return None


if __name__ == '__main__':
    print('This is a module')
