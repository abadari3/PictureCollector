from product import *
from inventory import *

i = 0

def make(current):
    title = str(current[0]['Title'])
    handle = title.replace(' ', '').lower().replace("-", "").replace("/", "")
    colors = []
    images = []
    sizes = [7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 13, 14, 15]
    body = ''
    vendor = 'Duca'
    type = 'Dress Shoe'
    price = []
    inventory = []
    for row in current:
        for i in range(len(sizes)):
            price.append(row['Price'])
            if row[str(sizes[i])] == 'X':
                inventory.append((1, 0))
            else:
                inventory.append((0, 0))
        colors.append((row['Color'], "https://raw.githubusercontent.com/abadari3/Shopify-Product-Manager/master/duca/" + row['Images']))
        images.append(("https://raw.githubusercontent.com/abadari3/Shopify-Product-Manager/master/duca/" + row['Images'], title + " " + row['Color']))
    
    tags = []
    sku = []
    for s in sizes:
        for c, i in colors:
            tc = "color:" + c
            sku.append((handle+"-"+str(s)+"-"+c.replace(' ', '')).lower())
            if tc not in tags:
                tags.append(tc)
        tags.append("size:" + str(s))

    seotitle = 'Brite Creations | ' + title + ' Fur.'
    seodescription = 'Shop at Brite Creations Atlanta for the best deal on ' + title + ' ' + 'fur.\n' + body

    return product(handle=handle, title=title, body=body, vendor=vendor, type=type, sizes=sizes, colors=colors, images=images, tags=tags, price=price, seotitle=seotitle, seodescription=seodescription, sku=sku, inventory=inventory)


products = []
with open("DUCA.csv", encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    prevtitle = ''
    current = []
    for row in reader:
        i += 1
        if row['Title'] != prevtitle and i != 1:
            products.append(make(current))
            current = []
        else:
            current.append(row)
        prevtitle = row['Title']
    make(current)

for p in products:
    print(p)

productstocsv(products)
productstoinventory(products)