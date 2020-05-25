import requests
from bs4 import BeautifulSoup
from os.path  import basename
import os
import re
import sys

main_link = sys.argv[1]
r = requests.get(main_link)
soup = BeautifulSoup(r.content, 'lxml')

links = soup.findAll('li', attrs={'class': ''})

for chapter, link in enumerate(links):
    resp = requests.get(link.a['href'])
    soup = BeautifulSoup(resp.content,'lxml') # choose lxml parser
    image_tags = soup.findAll('img')
    title = re.search("Chapter.*", link.a.text)
    path = main_link+"/"+title.group()
    if(not os.path.exists(path)):
        os.mkdir(basename(path))
    print(title)
    for number, image_tag in enumerate(image_tags):
        source = image_tag.get('src')
        filename = os.path.join(basename(path), str(number)+".jpg")
        print(filename)
        with open(filename, "wb") as f:
            f.write(requests.get(source).content)