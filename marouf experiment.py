from bs4 import BeautifulSoup
import csv
import time
import requests
from selenium import webdriver
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

csv_file = open("marouf_cars_second.csv", "w", encoding="utf-8")
writer = csv.writer(csv_file)
writer.writerow(["الفسم ", "مكان العمل", "عن العمل", "الموقع الالكتروني", "انستجرم", "تويتر",
                 "فيسبوك", "سناب شات ", "تليجرام", "البريد الالكتروني", "رقم الهاتف", "رقم الجوال"
                    , "واتس اب", "التقييم", "الرابط"])
csv_links = open("marouf_links_second.csv", "w", encoding="utf-8")
link_writer = csv.writer(csv_links)
link_writer.writerow(["links"])
page_link = "https://maroof.sa/134013"
path = r"C:\Program Files (x86)\geckodriver.exe"
driver = webdriver.Firefox(executable_path=path)
driver.get("https://maroof.sa/BusinessType/BusinessesByTypeList"
           "?bid=23&sortProperty=BestRating&DESC=True")
time.sleep(2)
driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
generate_pages = 1185
end_page = 0


def click_button(ganerate_page, end_page, drive):
    page_to_start = end_page
    time.sleep(15)
    try:
        for i in range(generate_pages - page_to_start):
            end_page = end_page + 1
            time.sleep(5)
            button = driver.find_element_by_id("loadMore")
            if button.is_displayed():
                if button.is_enabled():
                    button.click()
                else:
                    time.sleep(20)
                    print("try make it clickable")
                    button.click()
            else:
                time.sleep(30)
                print("wating and try again")
                button = driver.find_element_by_id("loadMore")
                button.click()

            print(end_page)
            driver.execute_script("arguments[0].click();", button)
    except:
        print("in the except ")
        end_page = end_page - 1
        pass

    return end_page, driver


a = 1
while generate_pages > end_page:
    print(" we are in loop", a)

    if a < 200:
        end_page, driver = click_button(generate_pages, end_page, driver)
    else:
        end_page = 200000
    a = a + 1

html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
soup = BeautifulSoup(html, "lxml")
page_links = []
partial_page_links = soup.find("div", id="list").findAll("a")
for partial_page_link in partial_page_links:
    link_writing = []
    mylink = "https://maroof.sa" + partial_page_link["href"]
    page_links.append(mylink)
    link_writing.append(mylink)
    link_writer.writerow(link_writing)
print(len(page_links))

num_page = 0


def get_page(page_link_getter):
    checker = False
    try:
        r = requests.get(page_link_getter)
        page_source = r.content
        soup = BeautifulSoup(page_source, "lxml")

        section = soup.find("div", class_="media-body media-body--width").find("p").text
        data = []
        place = soup.findAll("h3")
        if len(place) > 1:
            place_text = place[0].text + place[1].text
        else:
            place_text = place.text
        about_work = soup.find("div", class_="col-xs-12 withScroll").text
        evaluation = soup.find("div", class_="rating wrappe"
                                             "r-tool").findAll("span", class_="rating-num")[1].text
        website = None
        twitter = None
        mobile_phone = None
        telephone = None
        gmail = None
        telegram = None
        whats_up = None
        facebook = None
        instgram = None
        snapchat = None
        links = soup.findAll("div", class_="social-row")
        print(len(links))
        for link in links:
            info = link.find("div", class_="media-body")
            contacts = info.findAll("p", class_="text-primary")
            if len(contacts) >= 2:
                title = contacts[0].text
                value = contacts[1]

                if "الموقع الإلكتروني " in title:
                    website = value.text
                elif "تويتر" in title:
                    twitter = value.text
                elif "رقم الهاتف " in title:
                    mobile_phone = value.text
                elif "رقم الجوال " in title:
                    telephone = value.text
                elif "البريد الإلكتروني" in title:
                    gmail = value.text
                elif "تليجرام" in title:
                    telegram = value.text
                elif "واتس آب" in title:
                    whats_up = value.text
                elif "فيس بوك" in title:
                    facebook = value.text
                elif "إنستجرام" in title:
                    instgram = value.text
                elif "سناب شات" in title:
                    snapchat = value.text
                elif "Clouds Spa" in title:
                    instgram = value.text
                elif "انستقرام" in title:
                    instgram = value.text
                else:
                    print(title + "is not included in tour titles")
        data.append(section)
        data.append(place_text)
        data.append(about_work.replace("\n", "", 20))
        data.append(website)
        data.append(instgram)
        data.append(twitter)
        data.append(facebook)
        data.append(snapchat)
        data.append(telegram)
        data.append(gmail)
        data.append(mobile_phone)
        data.append(telephone)
        data.append(whats_up)
        data.append(evaluation)
        data.append(page_link)
        writer.writerow(data)

        checker = False
    except:
        pass
        checker = True
    return checker


for page_link in page_links:
    num_page = num_page + 1
    chec = True
    while chec:
        chec = get_page(page_link)
    print("exceeds page", num_page)
