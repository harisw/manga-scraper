import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from os.path  import basename
import time
import os
import re
import sys
import argparse

options = Options()
#options.headless = True
driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\DBLab\Documents\chromedriver\chromedriver.exe')
driver.maximize_window()
parser = argparse.ArgumentParser()
parser.add_argument("url", help="Specify root link")
parser.add_argument("chapter")
parser.add_argument("--continuous", help="Keep scraping until there is no more chapter")

parser = parser.parse_args()
suffix_link = "#nanogallery/my_nanogallery/0/1"
main_link = parser.url + suffix_link


#r = requests.get(main_link)
#scrolling
driver.get(main_link)
driver.implicitly_wait(3)
total = driver.find_element_by_class_name("pageCounter").get_attribute('innerHTML').strip()
# total = total.split("/")
# print(total)
# driver.quit()
# exit()
#total = int(total.split("/")) + 1
#chapter = main_link.split("=")[1]
chapter = parser.chapter
path = "../outputs/"+chapter
os.mkdir(basename(path))
old_source = ""
for page in range(1, 225):
    driver.implicitly_wait(1.5)
    source = driver.find_element_by_class_name("nGY2ViewerMedia").get_attribute('src')
    while old_source == source:
        driver.implicitly_wait(1)
        source = driver.find_element_by_class_name("nGY2ViewerMedia").get_attribute('src')


    print("Chapter " + str(chapter))
    filename = os.path.join(basename(path), str(bin(page))+".jpg")
    print("Page "+str(filename))
    with open(filename, "wb") as f:
        f.write(requests.get(source).content)
    driver.find_element_by_class_name("nGY2ViewerAreaNext").click()
    old_source = source
driver.quit()
# links = soup.findAll('li', attrs={'class': ''})

# for chapter, link in enumerate(links):
#     resp = requests.get(link.a['href'])
#     soup = BeautifulSoup(resp.content,'lxml') # choose lxml parser
#     image_tags = soup.findAll('img')
#     title = re.search("Chapter.*", link.a.text)
#     path = main_link+"/"+title.group()
#     if(not os.path.exists(path)):
#         os.mkdir(basename(path))
#     print(title)
#     for number, image_tag in enumerate(image_tags):
#         source = image_tag.get('src')
#         filename = os.path.join(basename(path), str(number)+".jpg")
#         print(filename)
#         with open(filename, "wb") as f:
#             f.write(requests.get(source).content)