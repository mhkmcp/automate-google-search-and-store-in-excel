import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

import googlemaps
import xlwt


def geocode_address(loc):
    gmaps = googlemaps.Client(key='AIzaSyC_YezsLXxNWVt8QgNcMJnNMRcWmPQmHDA')
    geocode_result = gmaps.geocode(loc)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    return lat, lon


driver = webdriver.Chrome(ChromeDriverManager().install())

wb = xlwt.Workbook()
ws = wb.add_sheet("test_sheet")

ws.write(0, 0, "Name")
ws.write(0, 1, "Address")
ws.write(0, 2, "Lat/Lon")
ws.write(0, 3, "District")
# ws.write(0, 4, "Rating")
# ws.write(0, 5, "Review")
# ws.write(0, 6, "Afluence")

all_districts = ["Dhaka", "Chittagong", "Sylhet", "Rajshahi", "Khulna", "Comilla", "Barishal",
                 "Mymensingh"]


# print(len(all_districts))
row_count = 1
restaurant_count = 0

for dst in all_districts:
    print(dst)

    WEBSITE_URL = "https://www.google.com/search?query=airport+{}".format(dst)
    print(WEBSITE_URL)

    try:
        driver.get(WEBSITE_URL)
        driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[2]/div/div[6]/div/g-more-link/a').click()
        time.sleep(1)

        restaurants = driver.find_elements_by_css_selector('#rl_ist0 > div.rl_tile-group > div.rlfl__tls.rl_tls > div')

        for restaurant in restaurants:
            name, rating, stars, reviews, address = "N/A", 0.0, 0, 0, "N/A"
            feature_count = 0
            try:
                name = restaurant.find_element_by_css_selector('.dbg0pd>div').text
                if '\n' in name:
                    name.replace('\n', '')
                if "airport" not in name:
                    continue

                feature_count += 1
                ws.write(row_count, 0, name)

                lat, lon = 0.0, 0.0
                try:
                    lat, lon = geocode_address(name)
                except Exception as ex:
                    print('Lat/Long issue')
                lat_lon = str(lat) + ", " + str(lon)

                ws.write(row_count, 2, lat_lon)
                ws.write(row_count, 3, dst)

            except Exception as ex:
                print(ex)
                continue

            try:
                detail = restaurant.find_element_by_css_selector('span.rllt__details')
                try:
                    rating = detail.find_element_by_css_selector('span.BTtC6e').text
                    feature_count += 1
                    ws.write(row_count, 4, rating)
                except Exception as ex:
                    print(ex)

                try:
                    stars = detail.find_element_by_css_selector('div:nth-child(1) > span:nth-child(4)').text
                    stars = len(stars)
                    feature_count += 1
                except Exception as ex:
                    print(ex)

                try:
                    address = detail.find_element_by_css_selector('div:nth-child(2) > span > span').text
                    address = address + " " + dst
                    feature_count += 1
                    ws.write(row_count, 1, name)
                except Exception as ex:
                    print(ex)

                try:
                    reviews = detail.find_element_by_css_selector('div:nth-child(1) > span:nth-child(3)').text
                    feature_count += 1
                    reviews = reviews[1:-1]
                    if ',' in reviews:
                        x, y = reviews.split(',')
                        reviews = x + y
                    reviews = int(reviews)
                    if reviews == 0 or "online" in name.lower() or "amazon" in name.lower():
                        row_count += 1
                        continue

                    ws.write(row_count, 5, reviews)
                except Exception as ex:
                    print(ex)

            except Exception as ex:
                print(ex)

            # ultra high 4.7 > $$$
            # high 4 > $$$
            # mid $$
            # low $

            # rating = float(rating)
            # reviews = int(reviews)
            # stars = int(stars)
            # print(type(rating), type(reviews), type(stars))
            # print(name, reviews, rating)
            # if rating >= 4.5 and reviews > 20 or stars == 3:
            #     ws.write(row_count, 6, "Ultra High")
            # elif rating < 4.0 and reviews >= 15 or stars >= 2:
            #     ws.write(row_count, 6, "High")
            # elif rating >= 3.7 and reviews > 10:
            #     ws.write(row_count, 6, "Mid")
            # else:
            #     ws.write(row_count, 6, "Low")

            row_count += 1
            restaurant_count = restaurant_count + 1

            print(name, address)

    except Exception as ex:
        print(ex)

wb.save("airport_list.xls")
print('Total Banks: ', restaurant_count)
