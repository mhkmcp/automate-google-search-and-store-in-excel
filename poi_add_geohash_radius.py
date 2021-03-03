import pygeohash as pgh
import googlemaps
import pandas as pd


def geocode_address(loc):
    gmaps = googlemaps.Client(key='AIzaSyC_YezsLXxNWVt8QgNcMJnNMRcWmPQmHDA')
    geocode_result = gmaps.geocode(loc)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    # print(lat, lon)
    return lat, lon


def get_hash(lat, long, precision):
    hash = pgh.encode(lat, long, precision)
    return hash


df = pd.read_csv('bd_poi_data_v2_build.csv', error_bad_lines=False)

row, col = str(df.shape)[1:-1].split(", ")
row, lon = int(row), int(col)
cnt = 0

for r in range(row):
    latitude = df.loc[r, 'latitude']
    longitude = df.loc[r, 'longitude']
    category = df.loc[r, 'category']

    if latitude < 21 or latitude > 24 or longitude < 88 or longitude > 93 or len(str(latitude)) < 2 or len(str(longitude)) < 2:
        df.loc[r, 'radius'] = 0
        df.loc[r, 'geohash'] = 0
        cnt += 1
    else:
        if category == "Hotel & Resort":
            precision = 7
            radius = 200
            geohash = get_hash(latitude, longitude, precision)
            df.loc[r, 'geohash'] = geohash
            df.loc[r, 'radius'] = radius

        elif category == "Hospital":
            precision = 6
            radius = 300
            geohash = get_hash(latitude, longitude, precision)
            df.loc[r, 'geohash'] = geohash
            df.loc[r, 'radius'] = radius

        elif category == "Shopping Mall":
            precision = 7
            radius = 300
            geohash = get_hash(latitude, longitude, precision)
            df.loc[r, 'geohash'] = geohash
            df.loc[r, 'radius'] = radius

        elif category == "Restaurant":
            precision = 9
            radius = 200
            geohash = get_hash(latitude, longitude, precision)
            df.loc[r, 'geohash'] = geohash
            df.loc[r, 'radius'] = radius

        elif category == "School":
            precision = 7
            radius = 300
            geohash = get_hash(latitude, longitude, precision)
            df.loc[r, 'geohash'] = geohash
            df.loc[r, 'radius'] = radius

    # & (df['latitude'] < 21) & df['latitude'] > 24)
    #     (df['longitude'] < 88) & (df['longitude'] > 93)
    #
    # print(df.head())
    # 200	fmvq7dx	Mid	Hotel & Resort
    # 300	wh0kp5	Low	Hospital
    # 300	wh0r39g		School
    # 300	9vu0p85	Low	Shopping Mall
    # 100	tek6pe2rt	High	Restaurant
    # df.loc[r, 'latitude'] = 50
    # print()
# print(row, type(col))
# print(df.iloc[:3, :])
df.to_csv('bd_v2_final_data.csv')
print(cnt)
