import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

import googlemaps
import xlwt
import pandas as pd


def geocode_address(loc):
    gmaps = googlemaps.Client(key='AIzaSyC_YezsLXxNWVt8QgNcMJnNMRcWmPQmHDA')
    geocode_result = gmaps.geocode(loc)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    # print(lat, lon)
    return lat, lon


driver = webdriver.Chrome(ChromeDriverManager().install())

# WEBSITE_URL = "https://en.wikipedia.org/"
WEBSITE_URL = "https://dhakaeducationboard.gov.bd/index.php/site/subdomain"
END_URL = "wiki/List_of_schools_in_Bangladesh"
LOC_URL = "wiki/List_of_educational_institutions_in_Barisal"

driver.get(WEBSITE_URL)
# time.sleep(1)
# driver.maximize_window()


wb = xlwt.Workbook()
ws = wb.add_sheet("test_sheet")

ws.write(0, 0, "Name")
ws.write(0, 1, "Category")
ws.write(0, 2, "Lat/Lon")
ws.write(0, 3, "District")

print("SUCCESS")
select = Select(driver.find_element_by_xpath('//*[@id="example2_length"]/label/select'))
select.select_by_visible_text('100')
time.sleep(1)
tr_no = 1
count = 0
page = 1
x_row = 1
f_count = 0
for _ in range(0, 65000):
    try:
        name = driver.find_element_by_xpath('//*[@id="example2"]/tbody/tr[' + str(tr_no) + ']/td[2]').text
        district = driver.find_element_by_xpath('//*[@id="example2"]/tbody/tr[' + str(tr_no) + ']/td[3]').text
        # if not name:
        #     name = driver.find_element_by_xpath(
        #         '//*[@id="mw-content-text"]/div/table/tbody/tr[' + str(tr_no) + ']/td[1]/a').text

        while "[" in name:
            name = name[:-1]

        lat, lon = 0.0, 0.0
        try:
            lat, lon = geocode_address(name)
        except Exception as ex:
            print('Lat/Long issue')
        print()
        lat_lon = str(lat) + ", " + str(lon)

        _name = name.lower()

        if "board" in _name:
            pass
        elif "school" in _name:
            print('Page: ', page, 'Tr: ', tr_no, 'Count: ', count, 'F Count: ', f_count)
            print('Name: ', name)
            print('Lat/Long: ', lat, lon)

            ws.write(x_row, 0, name)
            ws.write(x_row, 1, 'School')
            ws.write(x_row, 2, lat_lon)
            ws.write(x_row, 3, district)
            x_row += 1
            count += 1

        tr_no += 1
        f_count += 1

        if tr_no == 101:
            driver.find_element_by_xpath('//*[@id="example2_next"]/a').click()
            time.sleep(3)
            page += 1

        if f_count > 6300:
            break
    except Exception as ex:
        print(ex)
        tr_no = 1

wb.save("schools_list.xls")
print('Total Count: ', count)
