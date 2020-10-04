# handle = ""           one per product
# title = ""            one per product
# body = ""             one per product
# vendor = ""           one per product
# type = ""             one per product
# tags = []             must contain size tags and color tags
# sizes = []            list of sizes
# colors = []           list of tuples: (color, colorimg)
# price = []            price for each variant in order, first by size, then by color.
# images = []           list of tuples, (image url, alt text)
# sku = []              sku for each variant in order, first by size, then by color.
# inventory = []        list of tuples for inventory of each (online, retail) quantities

# requirements

# defaults:
    # vendor = "Winter Fur"
    # type = "Fur"
    # inventory = online = 1
    # sizes = [Small, Medium, Large, XL, 2XL, 3XL, 4XL, 5XL, 6XL, 7XL, 8XL]

# get from excel:
    # title
    # price
    # sku header
    # color 
    # url

# get from website:
    # body: fur details
    # images

# construct from collected info
    # handle
        # from title, add number if repeated title
    # body: add description to given text
        # <a href="https://britecreations.com/pages/about">Brite Creations</a> luxury winter fur contains the best quality responsibly sourced genuine mink, fox, and chinchilla fur. Winter fur items are fulfilled based on in-store stock availability. Depending on the style and size your order may take between 1-6 weeks. You will be updated via email and phone number regarding the status of your order. 
    # tags:
        # color tags
        # size tags

# modify before submission
    # price -> take single value and make into a list with size*color entries
    # sku -> take header value and make into a list with size*color entries. append size to each entry.
    # inventory -> take single tuple and make list of tuples with size*color entries
    
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

# for row in csv
    # title = row[title]
    # price = row[price]
    # 

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

import csv
from product import *
# from online import *
from inventory import *
from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup

globalhandles = []

def Create_Product(dictrow):
    global globalhandles
        # extend
    inventory = []
    sku = []
    price = []
    tags = []
    sizes=['Small', 'Medium', 'Large', 'XL', '2XL', '3XL', '4XL', '5XL', '6XL', '7XL', '8XL']
    for i in range(11):
        inventory.append((1, 0))
        sku.append(row['SKU'] + "-" + sizes[i])
        price.append(row['Price'])
        tags.append('size:' + sizes[i])
        # get title, and make handle. if title is a duplicate, then add number to handle.
    title = row['Title']
    handle = title.replace(' ', '').lower().replace("-", "").replace("/", "")
    if handle not in globalhandles:
        globalhandles.append(handle)
    else:
        handle += "1"
        if handle in globalhandles:
            handle += "1"
        globalhandles.append(handle)
    
    url = row['URL']

    body=""

        # get images and body from URL.
    # result = requests.get(url)
    # soup = BeautifulSoup(result.content, "html.parser")
    # details = soup.find("div", {"class": "tab-content tab-content--description"})
    # details = details.find("ul")
    # body = "<meta charset=\"utf-8\">\n" + str(details) + "\n"
    # body += "<a href=\"https://britecreations.com/pages/about\">Brite Creations</a> luxury winter fur contains the best quality responsibly sourced genuine mink, fox, and chinchilla fur. Winter fur items are fulfilled based on in-store stock availability. Depending on the style and size your order may take between 1-6 weeks. You will be updated via email and phone number regarding the status of your order."

    # img = soup.find("a", {"class": "MagicZoom"})
    images = [("https://upscalemenswear.com" + url, title)]

    # imglink = "https://upscalemenswear.com" + img['href']
    # response = requests.get(imglink)
    # image = Image.open(BytesIO(response.content))
    # x, y = image.size
    # xl = x//2 - x//20
    # xr = xl + x//10
    # yl = y//2 - y//20
    # yr = yl + y//10
    # image = image.crop((xl, yl, xr, yr))
    # image.save("pics/"+ ("fur " + row['Color']).lower().replace(' ', '-').replace('/', '-') +".png")


    colors = [("fur " + row['Color'], images[0][0])]
    tags.append('color:' + row['Color'])
    

    seotitle = 'Brite Creations | ' + title + ' Fur.'
    seodescription = 'Shop at Brite Creations Atlanta for the best deal on ' + title + ' ' + 'fur.\n' + body

    return products.append(product(handle=handle, title=title, body=body, vendor="Winter Fur", type="Fur", sizes=['Small', 'Medium', 'Large', 'XL', '2XL', '3XL', '4XL', '5XL', '6XL', '7XL', '8XL'], colors=colors, images=images, tags=tags, price=price, seotitle=seotitle, seodescription=seodescription, sku=sku, inventory=inventory))
    # still to do
    # body
    # images
        # save swatches to folder
    # seo description
    

products = []
i = 0
with open("Fur_import_2020.csv", encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        i += 1
        products.append(Create_Product(row))
        print(i)

# productstocsv(products)
# productstoinventory(products)