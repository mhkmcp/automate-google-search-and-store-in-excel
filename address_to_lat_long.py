import googlemaps
import pandas as pd


def geocode_address(loc):
    gmaps = googlemaps.Client(key='AIzaSyC_YezsLXxNWVt8QgNcMJnNMRcWmPQmHDA')
    geocode_result = gmaps.geocode(loc)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    # print(lat, lon)
    return lat, lon


school_name = "Solema Ahamed Junior Girls School, Jamalpur Sadar, Jamalpur"

print(school_name, geocode_address(school_name))
# geocode_address('Mirpur International Tutorial')
