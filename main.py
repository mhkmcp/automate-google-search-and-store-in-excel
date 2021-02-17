import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# from address_to_lat_long import geocode_address

import googlemaps
import pandas as pd


def geocode_address(loc):
    gmaps = googlemaps.Client(key='AIzaSyC_YezsLXxNWVt8QgNcMJnNMRcWmPQmHDA')
    geocode_result = gmaps.geocode(loc)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    # print(lat, lon)
    return lat, lon


driver = webdriver.Chrome(ChromeDriverManager().install())

WEBSITE_URL = "https://en.wikipedia.org/"
END_URL = "wiki/List_of_schools_in_Bangladesh"
LOC_URL = "wiki/List_of_educational_institutions_in_Barisal"

driver.get(WEBSITE_URL + END_URL)
time.sleep(1)
# driver.maximize_window()

print("SUCCESS")
# table_element = driver.find_element_by_class_name('wikitable')
trows = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/table/tbody/tr')
table_no = 1
tr_no = 1
count = 0
for _ in range(1, 1000):
    try:
        # // *[ @ id = "mw-content-text"] / div[1] / table[2] / tbody / tr[1] / td[1]
        name = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/table['+str(table_no)+']/tbody/tr['+str(tr_no)+']/td[1]').text
        if not name:
            name = driver.find_element_by_xpath(
                '//*[@id="mw-content-text"]/div/table['+str(table_no)+']/tbody/tr[' + str(tr_no) + ']/td[1]/a').text

        address = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/table['+str(table_no)+']/tbody/tr['+str(tr_no)+']/td[2]').text

        while "[" in name:
            name = name[:-1]

        print('Name: ', name)
        print('Address: ', address)
        try:
            lat, lon = geocode_address(name)
            print('Lat/Long: ', lat, lon)
        except Exception as ex:
            print('Lat/Long issue')
        print()
        count += 1
        tr_no += 1
    except Exception as ex:
        print(ex)
        tr_no = 1
        table_no += 1

    print('Table: ', table_no, 'Tr: ', tr_no)
    print()


print('Total Count: ', count)
# print(table_element)

# try:
#     element = driver.find_element_by_id("P826_BROWSE")
#     time.sleep(2)
#     element.send_keys('C://Users/zahad/Desktop/humayun/New/4_files/bank_asia_logo.png')
#     print("GOT IT")
# except Exception as e:
#     print(e)
#     print("Fi")