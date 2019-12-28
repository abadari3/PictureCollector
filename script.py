import os
import requests
import wget
from bs4 import BeautifulSoup
import string

def getpics(urllink):
    result = requests.get(urllink)

    # if successful parse the download into a BeautifulSoup object, which allows easy manipulation 
    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")

    pics = []
    os.mkdir("images")
    for link in soup.find_all("img"):
        title = link.get("alt")
        table = str.maketrans(dict.fromkeys(string.punctuation))
        title = title.translate(table)
        title = title.replace(" ", "_")
        title += ".jpg"
        title = "images\\" + title
        link = "http://www.maurishoes.com/dev/images/public/big/" + link.get("src")[22:]
        pics.append((title, link))

    for (t, l) in pics:
        # print(t + ": \n" + l + "\n")
        try:
            wget.download(l, t+".jpg")
        except:
            print(t + ": \n" + l + "\n")
            continue
    print("done")





getpics("http://www.maurishoes.com/usa-collection.html")