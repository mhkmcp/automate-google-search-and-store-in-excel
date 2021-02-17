import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import pandas as pd

import googlemaps
import xlwt
import pygeohash as pgh


def geocode_address(loc):
    gmaps = googlemaps.Client(key='AIzaSyC_YezsLXxNWVt8QgNcMJnNMRcWmPQmHDA')
    geocode_result = gmaps.geocode(loc)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    return lat, lon


def get_hash(lat, long, precision):
    hash = pgh.encode(lat, long, precision)
    # print(hash, type(hash))
    return hash


driver = webdriver.Chrome(ChromeDriverManager().install())

wb = xlwt.Workbook()
ws = wb.add_sheet("test_sheet")

# name, city, radius, lat, long, geohash, precision

ws.write(0, 0, "Name")
ws.write(0, 1, "City")
ws.write(0, 2, "Latitude")
ws.write(0, 3, "Longitude")
ws.write(0, 4, "Precision")
ws.write(0, 5, "Radius")
ws.write(0, 6, "Geohash_3")
ws.write(0, 7, "Geohash_4")
ws.write(0, 8, "Geohash_5")
ws.write(0, 9, "Geohash_6")

df = pd.read_excel('all_thana_master_list.xlsx')
# print(df.iloc[3:10, 3:-1])

count = 0
for row in range(2, 550):
    thana = df.iloc[row, 4]
    while '(' in thana:
        thana = thana[:-1]
    area = df.iloc[row, 3]
    area = area.split(' ')[0]
    query = thana + "+Upazila+" + area

    print(row, ' ', query)
    WEBSITE_URL = "https://www.google.com/search?query={}".format(query)
    driver.get(WEBSITE_URL)
    volume, radius = 0, 0
    time.sleep(1)
    found = False

    try:                                   # j //*[@id="kp-wp-tab-overview"]/div[1]/div/div/div/div[1]/div/div/div/span[2]
        volume = driver.find_element_by_xpath('//*[@id="kp-wp-tab-overview"]/div[1]/div/div/div/div[2]/div/div/div/span[2]').text
        volume = volume.split(' ')[0]
        if ',' in volume:
            x, y = volume.split(',')[0], volume.split(',')[1]
            volume = x + y
        volume = float(volume)
        # print(volume, type(volume))
        radius = volume ** 0.5
        print(radius, volume)
        found = True
    except Exception as ex:
        pass

    if not found:
        try:                                   # j //*[@id="kp-wp-tab-overview"]/div[1]/div/div/div/div[1]/div/div/div/span[2]
            volume = driver.find_element_by_xpath('//*[@id="kp-wp-tab-overview"]/div[1]/div/div/div/div[1]/div/div/div/span[2]').text
            volume = volume.split(' ')[0]

            if ',' in volume:
                x, y = volume.split(',')[0], volume.split(',')[1]
                volume = x + y
            volume = float(volume)
            # print(volume, type(volume))
            radius = volume ** 0.5
            print(radius, volume)
            found = True

        except Exception as ex:
            pass

    precision = 9
    # print(volume, type(volume))
    if isinstance(volume, str):
        volume = 0
    if volume <= 100:
        precision = 6
    if 100 < volume <= 350:
        precision = 5
    if 351 < volume <= 700:
        precision = 4
    if 701 < volume:
        precision = 3

    latitude, longitude, hash = 0, 0, '#'

    if not found:
        print('0')
        count += 1
    else:
        latitude, longitude = geocode_address(query)
        latitude = float(latitude)
        longitude = float(longitude)
        hash = get_hash(latitude, longitude, precision)
        print('1')

    ws.write(row-1, 0, thana)
    ws.write(row-1, 1, area)
    ws.write(row-1, 2, latitude)
    ws.write(row-1, 3, longitude)
    ws.write(row-1, 4, precision)
    ws.write(row-1, 5, radius)

    if precision == 3:
        ws.write(row-1, 6, hash)
    elif precision == 4:
        ws.write(row-1, 7, hash)
    elif precision == 5:
        ws.write(row-1, 8, hash)
    elif precision == 6:
        ws.write(row-1, 9, hash)


wb.save("all_thana_list.xls")
print('\nMissing Area ', count, ' Thana')

# 24.565971, 91.854552

# WEBSITE_URL = "https://www.google.com/search?query=hospital+clinic+{}".format(dst)

# name, city, radius, lat, long, geohash, precision
# < 100
#     6
# 100 < x< 350:
#     5
# 351 < x < 700:
#     4
# 701 < x < any:
#     3

# 22.214259, 92.336789
