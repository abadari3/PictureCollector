from product import *
from inventory import *
import numpy as np
import csv
from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import os.path
from os import path
from random import randrange

i = 0

def make(current):
    title = str(current[0]['Title'])
    handle = title.replace(' ', '').lower().replace("-", "").replace("/", "")
    colors = []
    images = []
    sizes = [7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 13, 14, 15]
    body = '<ul>\n<li><b>Material: </b> ' + current[0]['Material'] +' Leather</li>\n<li><b>Color: </b>Blue Navy</li>\n<li><b>Outer Sole: </b>Leather</li>\n<li>Comes with original box and dustbag</li>\n<li>Made in Italy</li><br>\n<li>Duca Shoes generally run about half size bigger than listed. We recommend purchasing a half-size or full size smaller from your normal size.</li>\n</ul>'
    vendor = 'Emilio Franco'
    type = 'Dress Shoe'
    price = []
    inventory = np.zeros((10, 14))
    c = -1
    for row in current:
        c += 1
        for i in range(len(sizes)):
            price.append(row['Price'])
            if row[str(sizes[i])] == 'X':
                inventory[c][i] = 1
            else:
                inventory[c][i] = 0
        colors.append((row['Color'], "https://raw.githubusercontent.com/abadari3/Shopify-Product-Manager/master/duca/" + row['Images']))
        images.append(("https://raw.githubusercontent.com/abadari3/Shopify-Product-Manager/master/duca/" + row['Images'], title + " " + row['Color']))
    
    inv = []
    for row in inventory:
        if 1 in row:
            inv.append(row)
    inv = np.array(inv).T
    finv = []
    for a in inv.ravel():
        finv.append((int(a), 0))
    # print(finv)
    tags = []
    sku = []
    for s in sizes:
        for c, i in colors:
            tc = "color:" + c
            sku.append((handle+"-"+str(s)+"-"+c.replace(' ', '')).lower())
            if tc not in tags:
                tags.append(tc)
        tags.append("size:" + str(s))

    # print(inventory)


    seotitle = 'Brite Creations | ' + title + ' Fur.'
    seodescription = 'Shop at Brite Creations Atlanta for the best deal on ' + title + ' ' + 'fur.\n' + body

    return product(handle=handle, title=title, body=body, vendor=vendor, type=type, sizes=sizes, colors=colors, images=images, tags=tags, price=price, seotitle=seotitle, seodescription=seodescription, sku=sku, inventory=finv)


products = []
with open("EMILIOFRANCO.csv", encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    prevtitle = ''
    current = []
    for row in reader:
        i += 1
        print(row)
        if row['Title'] != prevtitle and i != 1 and len(current) != 0:
            products.append(make(current))
            current = []
        else:
            current.append(row)
        prevtitle = row['Title']
    make(current)

for p in products:
    for c, i in p.colors:
        response = requests.get(i)
        image = Image.open(BytesIO(response.content))
        x, y = image.size
        xl = 0.3*x
        xr = 0.4*x
        yl = .46*y
        yr = .56*y

        r=.5
        
        xl = (xl + xr)/2-r*(xr-xl)/2
        xr = (xl + xr)/2+r*(xr-xl)/2
        yl = (yl + yr)/2-r*(yr-yl)/2
        yr = (yl + yr)/2+r*(yr-yl)/2
        image = image.crop((xl, yl, xr, yr))
        pt = "swatches/"+ c.lower().replace(' ', '-').replace('/', '-')

        if path.exists(pt):
            image.save(pt + str(randrange(10)) +".png")
        else:
            image.save(pt +".png")

productstocsv(products)
# productstoinventory(products)
