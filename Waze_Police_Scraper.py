import json
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from browsermobproxy import Server
from requests.exceptions import MissingSchema
import requests
import timeit
import time
import folium
import subprocess
import platform
from datetime import datetime

print("""Waze Police Scraper

Waze Police Scraper will open the Mozilla Firefox browser, onto Waze's live map website.
It'll scrape all the police's locations from your preferred location, by moving the mouse to that location. It also scrapes police traps.
Every cop that's scraped also has its own dataset. It has all the geographic location, but also the number of up votes on its existence by Waze's users, confidence, and reliability, by Waze itself.
Sometimes speed can also be included.
You can view all that in the map that will be generated after the program finished scraping.

Instructions:

Choose how much seconds do you want the program to scrape police. That time is for the user to move to another location, to scrape police vehicles / Traps reported by Waze's users.
If you press Enter, without entering any number, the number will be the default, 5 seconds, which is also the recommended value.
After the Firebox browser launched and you're done scraping, just close the browser, and wait 5 seconds.
After that, go to localhost:5000 or 127.0.0.1:5000 and you'll be presented with a map showing all the scraped police, and by clicking on them you'll be able to see more information on them like coordinates,
type of police (vehicle or trap), speed, number of up votes by Waze's users, and confidence and reliability estimated by Waze.
Also, you can download the scraped data as JSON, XLS (Excel), and CSV.
""")


def clear_screen():
    if platform.system() == "Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:  # Linux and Mac
        print("\033c", end="")


def save_config():
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = "config.config"
    f = open(file_name,
             "w")  # Don't need to check if file exists, because if it's not, the mode "w" will create it anyway.
    f.write(date)


def personalised_info():
    auto_or_manual = input(
        "Do you want the software to scrape the waze map Automatically? (Answer with 'a') ")  # Pretty much useless becasue there is no other option

    sec = input(
        "Every how much seconds do you want the scraper to scrape the data? maximum is 30 seconds, while minimum is 5 seconds. By not inputting anything the value will be set to the recommended value of 5 seconds. ")
    save_config()
    return auto_or_manual, sec


def start_server():
    global server, proxy, driver
    dict = {'port': 8080}
    server = Server("...")

    server.start()
    proxy = server.create_proxy()

    # proxy.wait_for_traffic_to_stop(6000, 9000)

    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    driver = webdriver.Firefox(executable_path="...",
        firefox_profile=profile)
    # Navigate to the application home page
    driver.get("https://www.waze.com/livemap?utm_source=waze_website&utm_campaign=waze_website")

    return driver


urls = []
count = 1
good_index = []
data_parsed = {}
inner_nested_data_parsed = {}
data_list = []
key_counts_with_subtype = []


def get_data(sec):
    global count, inner_nested_data_parsed
    start = timeit.timeit()  # Measure time
    # tag the har(network logs) with a name
    har = proxy.new_har("waze_{0}.format(i)")
    # Finding the URL requests where the data is stored in JSON format
    har = str(har)
    str_1 = "https://www.waze.com/il-rtserver/web/TGeoRSS?"
    str_2 = "&types=alerts%2Ctraffic%2Cusers"
    indx_1 = har.find(str_1)
    indx_2 = har.find(str_2)
    url = har[indx_1:indx_2]
    url = url + str_2
    urls.append(url)
    print(len(urls))
    # Loading data
    for d in urls:
        if d == str_2:  # User does not move
            print("Please move to your preffered location.")
            urls.remove(d)
            pass
        else:
            data = requests.get(url)
            data = data.text
            if not "DOCTYPE" in data:
                data = json.loads(data)
                print(type(data))
                end = timeit.timeit()  # Measure time
                print("Time Taken to fetch the data: {} seconds".format(end - start))  # Time to get data
                urls.remove(d)
                # Finding indexes to scrape
                for x in range(len(data["alerts"])):
                    if data["alerts"][x]["type"] == "POLICE":
                        good_index.append(x)
                    # Scraping data
                print(len(good_index))
                for x in good_index:
                    inner_nested_data_parsed["type_"] = (data["alerts"][x]["type"])
                    if data["alerts"][x]["subtype"]:
                        inner_nested_data_parsed["subtype"] = (data["alerts"][x]["subtype"])
                    else:
                        pass
                    inner_nested_data_parsed["country"] = (data["alerts"][x]["country"])
                    inner_nested_data_parsed["nThumbsUp"] = (data["alerts"][x]["nThumbsUp"])
                    inner_nested_data_parsed["confidence"] = (data["alerts"][x]["confidence"])
                    inner_nested_data_parsed["reliability"] = (data["alerts"][x]["reliability"])
                    inner_nested_data_parsed["speed"] = (data["alerts"][x]["speed"])
                    inner_nested_data_parsed["location_x"] = (data["alerts"][x]["location"]["x"])
                    print((data["alerts"][x]["location"]["x"]))
                    inner_nested_data_parsed["location_y"] = (data["alerts"][x]["location"]["y"])
                    print((data["alerts"][x]["location"]["y"]))
                    data_parsed[count] = inner_nested_data_parsed
                    print(data_parsed)
                    data_list.append(data_parsed)
                    inner_nested_data_parsed = {}
                    count += 1
            else:
                print("Data is inaccessible, wait {} seconds to to try again.".format(sec))
    print("Scraped {} Policeman / Police cars.".format(count - 1))  # Count equels one, so subtract
    return data_list


def map(key_counts_with_subtype, data_list):
    global data_parsed

    k = 0

    m = folium.Map(  # Map configuration
        location=[45.372, -121.6972],
        zoom_start=12, smooth_factor=2
    )

    tooltip = 'POLICE'  # Will be "subtype" and if "subtype" == "", than it'll be "type_"

    # Checking if subtype exists, and if he is, in what index of the data
    for x in data_list:
        for key in x.keys():
            try:
                if data_list[0][key]["subtype"]:
                    key_counts_with_subtype.append(key)
            except KeyError:
                pass

    for iter_2 in range(len(data_list)):
        data_parsed = data_list[iter_2]
    for key_count in range(1, len(data_parsed) + 1):

        try:
            if key_count == key_counts_with_subtype[key_count - 1]:  # Index starts from zero
                subtype = data_parsed[key_count]["subtype"]
            else:
                type_ = data_parsed[key_count]["type_"]
        except IndexError:  # There's no more elements in 'key_counts_with_subtype' list
            print(key_count, type(key_count))
            type_ = data_parsed[key_count]["type_"]
        country = data_parsed[key_count]["country"]
        nThumbsUp = data_parsed[key_count]["nThumbsUp"]
        confidence = data_parsed[key_count]["confidence"]
        reliability = data_parsed[key_count]["reliability"]
        speed = data_parsed[key_count]["speed"]
        location_x = data_parsed[key_count]["location_x"]
        location_y = data_parsed[key_count]["location_y"]
        try:
            if int(key_count) == key_counts_with_subtype[int(key_count) - 1]:
                string = '<i>subtype: <b>{0}</b>\ncountry: <b>{1}</b>\nnThumbsUp: <b>{2}</b>\nconfidence: <b>{3}</b>\nreliability: <b>{4}</b>\nspeed: <b>{5}</b>\nlocation x: <b>{6}</b>\nlocation y: <b>{7}</b></i>'.format(
                    subtype, country, nThumbsUp, confidence, reliability, speed, location_x, location_y)
            else:
                string = '<i>type: <b>{0}</b>\ncountry: <b>{1}</b>\nnThumbsUp: <b>{2}</b>\nconfidence: <b>{3}</b>\nreliability: <b>{4}</b>\nspeed: <b>{5}</b>\nlocation_x: <b>{6}</b>\nlocation_y: <b>{7}</b></i>'.format(
                    type, country, nThumbsUp, confidence, reliability, speed, location_x, location_y)
        except IndexError:  # There's no more elements in 'key_counts_with_subtype' list
            string = '<i>type: <b>{0}</b>\ncountry: <b>{1}</b>\nnThumbsUp: <b>{2}</b>\nconfidence: <b>{3}</b>\nreliability: <b>{4}</b>\nspeed: <b>{5}</b>\nlocation x: <b>{6}</b>\nlocation y: <b>{7}</b></i>'.format(
                type, country, nThumbsUp, confidence, reliability, speed, location_x, location_y)

        folium.Marker([location_y, location_x], popup=folium.Popup(string, max_width=450), tooltip=tooltip).add_to(m)

    m.save('templates//map.html')


def start_script():
    auto_or_manual, sec = personalised_info()
    err = False
    if auto_or_manual == "A" or auto_or_manual == "a":
        if sec.isdigit():  # Could have contained all than in a function
            driver = start_server()
            while not err:
                try:
                    title = driver.title  # Checking if user didn't close FireFox
                    time.sleep(int(sec))
                    try:
                        data_list = get_data(sec)
                    except KeyboardInterrupt:
                        exit()  # Cleaning the errors when the user wants to quit
                    f = open("C:\\Users\\Yahav Bahat\\Downloads\\ghgh.txt", "w", encoding="utf-8")
                    f.write(str(data_list))
                except (WebDriverException, MissingSchema):
                    err = True
                    if data_list:
                        print("Done scraping... Generating map..")
                        map(key_counts_with_subtype, data_list)
                        clear_screen()
                    else:
                        print(
                            "You didn't scraped anything. One possible explanation is that you didn't move with the mouse at all, or you closed the browser before the site completely loaded and the program didn't began to scrape.")
                        exit()
        else:
            sec = 5  # Default sec
            driver = start_server()
            while not err:
                try:
                    title = driver.title  # Checking if user didn't close FireFox
                    time.sleep(sec)
                    try:
                        data_list = get_data(sec)
                    except KeyboardInterrupt:
                        exit()  # Cleaning the errors when the user wants to quit
                    f = open("C:\\Users\\Yahav Bahat\\Downloads\\ghgh.txt", "w", encoding="utf-8")
                    f.write(str(data_list))
                except (WebDriverException, MissingSchema):
                    err = True
                    if data_list:
                        print(
                            "Done scraping... Generating map..")  # TODO: Remember to wait 5 seconds after closing the browser
                        map(key_counts_with_subtype, data_list)
                        clear_screen()
                    else:
                        print(
                            "You didn't scraped anything. One possible explanation is that you didn't move with the mouse at all, or you closed the browser before the site completely loaded and the program didn't began to scrape.")
                        exit()
    else:
        print("What was that? Try agian")
        exit()
