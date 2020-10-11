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

vendor = 'Fennix'

def make(current):
    title = str(current[0]['Title'])
    handle = title.replace(' ', '').lower().replace("-", "").replace("/", "")
    colors = []
    images = []
    sizes = list(current[0].keys())[5:-1]
    global vendor
    
    body = '<ul>\n<li><b>Material: </b> ' + current[0]['Material'] +' Leather</li>\n<li><b>Vendor: </b> ' + vendor +' </li>\n<li><b>Outer Sole: </b> Leather </li>\n<li>Comes with original box and dustbag</li>\n<li>Made in Italy</li><br>\n<li>Best quality and price from <a href=\"https://britecreations.com/pages/about\">Brite Creations Atlanta</a>.</li>\n</ul>'
    if vendor == 'Duca':
        body = body[:-5]
        body += '<br><li>Duca Shoes generally run about half size bigger than listed. We recommend purchasing a half-size or full size smaller from your normal size.</li></ul>'
    type = 'Dress Shoe'
    price = []
    inventory = np.zeros((15, len(sizes)))
    c = -1
    for row in current:
        c += 1
        for i in range(len(sizes)):
            price.append(row['Price'])
            if row[str(sizes[i])] == 'X':
                inventory[c][i] = 1
            else:
                inventory[c][i] = 0
        colors.append((row['Color'], "https://raw.githubusercontent.com/abadari3/Shopify-Product-Manager/master/" + vendor.lower().replace(' ', '') + "/" + row['Images'].strip()))
        images.append(("https://raw.githubusercontent.com/abadari3/Shopify-Product-Manager/master/" + vendor.lower().replace(' ', '') + "/" + row['Images'].strip(), title + " " + row['Color']))
    
    inv = []
    i=0
    for row in inventory:
        if i <= c:
            inv.append(row)
        i+=1
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


    seotitle = 'Brite Creations | ' + title + " " + type +' by ' + vendor
    seodescription = 'Shop at Brite Creations Atlanta for the best deal on ' + title + " " + type +' by ' + vendor + '\n' + body

    return product(handle=handle, title=title, body=body, vendor=vendor, type=type, sizes=sizes, colors=colors, images=images, tags=tags, price=price, seotitle=seotitle, seodescription=seodescription, sku=sku, inventory=finv)


products = []
with open( vendor.upper().replace(' ', '') + "MISC.csv", encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    prevtitle = ''
    current = []
    for row in reader:
        i += 1
        # print(row)
        if row['Title'] != prevtitle and i != 1 and len(current) != 0:
            products.append(make(current))
            current = [row]
        else:
            current.append(row)
        prevtitle = row['Title']
    products.append(make(current))

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

# productstocsv(products)
# productstoinventory(products)
