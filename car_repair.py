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
ws.write(0, 2, "Latitude")
ws.write(0, 3, "Longitude")
ws.write(0, 4, "District")
ws.write(0, 5, "Rating")


all_districts = ["Rajbari", "Barisal", "Sylhet", "Barguna", "Bhola", "Jhalokati", "Patuakhali", "Pirojpur", "Bandarban",
                 "Brahmanbaria", "Chandpur", "Chittagong", "Comilla", "Cox's Bazar", "Feni", "Khagrachhari",
                 "Lakshmipur", "Noakhali", "Rangamati", "Dhaka", "Faridpur", "Gazipur", "Gopalganj",
                 "Kishoreganj", "Madaripur", "Manikganj", "Munshiganj", "Narayanganj", "Narsingdi",
                 "Shariatpur", "Tangail", "Bagerhat", "Chuadanga", "Jessore", "Jhenaidah",
                 "Khulna", "Kushtia", "Magura", "Meherpur", "Narail", "Satkhira", "Jamalpur", "Mymensingh",
                 "Netrokona", "Sherpur", "Bogra", "Joypurhat", "Naogaon", "Natore", "Chapainawabganj",
                 "Pabna", "Rajshahi", "Sirajganj", "Dinajpur", "Gaibandha", "Kurigram", "Lalmonirhat",
                 "Nilphamari", "Panchagarh", "Rangpur", "Thakurgaon", "Habiganj", "Moulvibazar",
                 "Sunamganj"]

# "Barisal",

print(len(all_districts))

row_count = 1
restaurant_count = 0

for dst in all_districts[:10]:
    try:

        # WEBSITE_URL = "https://www.google.com/search?query=Car+Repair+Service+{}".format(dst)
        WEBSITE_URL = "https://www.google.com/search?query=Car+Showroom+{}".format(dst)
        print(WEBSITE_URL)

        driver.get(WEBSITE_URL)
        # time.sleep(1)
        driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[2]/div/div[6]/div/g-more-link/a').click()
        # driver.refresh()
        time.sleep(1)

        restaurants = driver.find_elements_by_css_selector('#rl_ist0 > div.rl_tile-group > div.rlfl__tls.rl_tls > div')

        for restaurant in restaurants:
            name, rating, stars, reviews, address = "N/A", 0.0, 0, 0, "N/A"
            feature_count = 0
            try:
                name = restaurant.find_element_by_css_selector('.dbg0pd>div').text
                if '\n' in name:
                    name.replace('\n', '')
                feature_count += 1
                ws.write(row_count, 0, name)

                lat, lon = 0.0, 0.0
                try:
                    lat, lon = geocode_address(name)
                    ws.write(row_count, 2, lat)
                    ws.write(row_count, 3, lon)
                except Exception as ex:
                    print('Lat/Long issue')
                lat_lon = str(lat) + ", " + str(lon)

                ws.write(row_count, 4, dst)

            except Exception as ex:
                print(ex)
                continue

            try:
                detail = restaurant.find_element_by_css_selector('span.rllt__details')
                try:
                    rating = detail.find_element_by_css_selector('span.BTtC6e').text
                    feature_count += 1
                    ws.write(row_count, 5, rating)
                except Exception as ex:
                    print(ex)

                # try:
                #     stars = detail.find_element_by_css_selector('div:nth-child(1) > span:nth-child(4)').text
                #     stars = len(stars)
                #     feature_count += 1
                # except Exception as ex:
                #     print(ex)

                try:
                    address = detail.find_element_by_css_selector('div:nth-child(2) > span > span').text
                    address = address + " " + dst
                    feature_count += 1
                    ws.write(row_count, 1, name)
                except Exception as ex:
                    print(ex)

                # try:
                #     reviews = detail.find_element_by_css_selector('div:nth-child(1) > span:nth-child(3)').text
                #     feature_count += 1
                #     reviews = reviews[1:-1]
                #     if ',' in reviews:
                #         x, y = reviews.split(',')
                #         reviews = x + y
                #     reviews = int(reviews)
                #     if reviews == 0 or "online" in name.lower() or "amazon" in name.lower():
                #         row_count += 1
                #         continue
                #
                #     ws.write(row_count, 5, reviews)
                # except Exception as ex:
                #     print(ex)

            except Exception as ex:
                print(ex)

            row_count += 1
            restaurant_count = restaurant_count + 1

            print(name, address, reviews)

    except Exception as ex:
        print(ex)

wb.save("car_showroom_list.xls")
print('Total Banks: ', restaurant_count)