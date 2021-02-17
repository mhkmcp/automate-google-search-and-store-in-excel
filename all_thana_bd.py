import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

import googlemaps
import xlwt
import pygeohash as pgh
import pandas as pd
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def geocode_address(loc):
    gmaps = googlemaps.Client(key='AIzaSyC_YezsLXxNWVt8QgNcMJnNMRcWmPQmHDA')
    geocode_result = gmaps.geocode(loc)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    return lat, lon


def get_hash(lat, long, precision):
    hash = pgh.encode(lat, long, precision)
    return hash


print(get_hash(22.4978576, 91.3553851, 11))


def get_rol_col(df):
    x, y = df.shape
    return int(x), int(y)


# df1 = pd.read_csv('BD_thana.csv', error_bad_lines=False)
# df2 = pd.read_excel('all_thana_list.xlsx')
#
# x1, y1 = get_rol_col(df1)
# x2, y2 = get_rol_col(df2)
#
# print(get_rol_col(df1), get_rol_col(df2))
#
# count = 1
#
# for idx1 in range(0, x1):
#     for idx2 in range(0, x2):
#         if df1.at[idx1, 'thana'] == df2.at[idx2, 'Name'] and df2.at[idx2, 'Radius'] != 0:
#             count += 1
#             df1.at[idx1, 'lat'] = df2.at[idx2, 'Latitude']
#             df1.at[idx1, 'long'] = df2.at[idx2, 'Longitude']
#             df1.loc[idx1, 'geohash'] = get_hash(df2.at[idx2, 'Latitude'], df2.at[idx2, 'Longitude'], 11)
#             print(df1.at[idx1, 'thana'], df2.at[idx2, 'Name'], idx1, idx2)
#
#
# datatoexcel = pd.ExcelWriter('BD_thana_list.xlsx')
#
# # write DataFrame to excel
# df1.to_excel(datatoexcel)
#
# # save the excel
# datatoexcel.save()
# # df1.to_csv('BD_thana_list.csv')
# print('Total Matched: ', count)
