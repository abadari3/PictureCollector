from product import product
import requests
import csv

from PIL import Image
from io import BytesIO

def newProduct(rows):
    if len(rows) == 0:
        return None
    r = rows.pop(0)
    handle = r['Handle']
    title = r['Title']
    body = r['Body (HTML)']
    vendor = r['Vendor']
    type = r['Type']
    tags = str(r['Tags']).split(',')
    sizes = [str(r['Option1 Value'])]
    colors = [(str(r['Option2 Value']), str(r['Variant Image']))]
    price = [r['Variant Price']]
    oldprice = [r['Variant Compare At Price']]
    barcode = [r['Variant Barcode']]
    images = [(r['Image Src'], r['Image Alt Text'])]
    seotitle = r['SEO Title']
    seodescription = r['SEO Description']
    sku = [r['Variant SKU']]
    published = r['Published']
    taxable = r['Variant Taxable']
    for row in rows:
        if row['Option1 Value'] not in sizes and row['Option1 Value'] != '':
            sizes.append(row['Option1 Value'])
        if (row['Option2 Value'], row['Variant Image']) not in colors and row['Option2 Value'] != '':
            colors.append((row['Option2 Value'], row['Variant Image']))
        if row['Image Src'] not in images and row['Image Src'] != '':
            images.append((row['Image Src'], row['Image Alt Text']))
        # colors, images, variant images, barcodes'
        barcode.append(row['Variant Barcode'])
        sku.append(row['Variant SKU'])
        price.append(row['Variant Price'])
        oldprice.append(row['Variant Compare At Price'])

            
    return product(handle=handle, title=title, body=body, vendor=vendor, type=type, tags=tags, sizes=sizes, colors=colors, price=price, oldprice=oldprice, barcode=barcode, images=images, seotitle=seotitle, seodescription=seodescription, sku=sku, published=published, taxable=taxable)

def csvtoproducts(file):
    products = []
    with open(file, encoding='unicode_escape') as csvfile:
        reader = csv.DictReader(csvfile)
        current = []
        i = 0
        for row in reader:
            i+= 1

            if row['Title'] != "":
                products.append(newProduct(current))
                current = []
                current.append(row)
            else:
                current.append(row)
        products.append(newProduct(current))
        products.pop(0)
        return products

def formattags(tags):
    out = ""
    for t in tags:
        out += t + ","
    out = out[:-1]
    return out

def getrows(prod):
    rows = []
    # first row
    # missing functionality of sizes, colors, images, variant images, 
    ssss = "Size"
    if 'Default Title' in prod.sizes:
        ssss = "Title"
    firstrow = {
        'Handle': prod.handle,
        'Title': prod.title, 
        'Body (HTML)': prod.body, 
        'Vendor': prod.vendor, 
        'Type': prod.type, 
        'Tags': formattags(prod.tags), 
        'Published':prod.published, 
        'Option1 Name':ssss, 
        'Option1 Value':'', 
        'Option2 Name':'', 
        'Option2 Value':'', 
        'Option3 Name':'', 
        'Option3 Value':'', 
        'Variant SKU':'', 
        'Variant Grams':'0', 
        'Variant Inventory Tracker':'shopify', 
        'Variant Inventory Policy':'deny', 
        'Variant Fulfillment Service':'manual', 
        'Variant Price': '', 
        'Variant Compare At Price': '', 
        'Variant Requires Shipping': 'TRUE', 
        'Variant Taxable':prod.taxable, 
        'Variant Barcode':'', 
        'Image Src': '', 
        'Image Position': '', 
        'Image Alt Text': '', 
        'Gift Card': 'FALSE', 
        'SEO Title': prod.seotitle, 
        'SEO Description': prod.seodescription, 
        'Google Shopping / Google Product Category': '', 
        'Google Shopping / Gender': '', 
        'Google Shopping / Age Group': '', 
        'Google Shopping / MPN': '', 
        'Google Shopping / AdWords Grouping': '', 
        'Google Shopping / AdWords Labels': '', 
        'Google Shopping / Condition': '', 
        'Google Shopping / Custom Product': '', 
        'Google Shopping / Custom Label 0': '', 
        'Google Shopping / Custom Label 1': '', 
        'Google Shopping / Custom Label 2': '', 
        'Google Shopping / Custom Label 3': '', 
        'Google Shopping / Custom Label 4': '', 
        'Variant Image': '', 
        'Variant Weight Unit': 'lb', 
        'Variant Tax Code': '', 
        'Cost per item': ''
    }
    rows.append(firstrow)
    # rest of the rows
    cn = len(prod.colors)
    if cn == 0:
        cn = 1
    cn *= len(prod.sizes)
    for i in range(cn - 1):
        row = {
            'Handle': prod.handle,
            'Title': '', 
            'Body (HTML)': '', 
            'Vendor': '', 
            'Type': '', 
            'Tags': '', 
            'Published':'', 
            'Option1 Name':'', 
            'Option1 Value':'', 
            'Option2 Name':'', 
            'Option2 Value':'', 
            'Option3 Name':'', 
            'Option3 Value':'', 
            'Variant SKU':'', 
            'Variant Grams':'0', 
            'Variant Inventory Tracker':'shopify', 
            'Variant Inventory Policy':'deny', 
            'Variant Fulfillment Service':'manual', 
            'Variant Price': '', 
            'Variant Compare At Price': '', 
            'Variant Requires Shipping': 'TRUE', 
            'Variant Taxable':prod.taxable, 
            'Variant Barcode':'', 
            'Image Src': '', 
            'Image Position': '', 
            'Image Alt Text': '', 
            'Gift Card': '', 
            'SEO Title': '', 
            'SEO Description': '', 
            'Google Shopping / Google Product Category': '', 
            'Google Shopping / Gender': '', 
            'Google Shopping / Age Group': '', 
            'Google Shopping / MPN': '', 
            'Google Shopping / AdWords Grouping': '', 
            'Google Shopping / AdWords Labels': '', 
            'Google Shopping / Condition': '', 
            'Google Shopping / Custom Product': '', 
            'Google Shopping / Custom Label 0': '', 
            'Google Shopping / Custom Label 1': '', 
            'Google Shopping / Custom Label 2': '', 
            'Google Shopping / Custom Label 3': '', 
            'Google Shopping / Custom Label 4': '', 
            'Variant Image': '', 
            'Variant Weight Unit': 'lb', 
            'Variant Tax Code': '', 
            'Cost per item': ''
        }
        rows.append(row)
    
    if len(prod.images) > cn:
        for j in range(len(prod.images) - cn):
            row = {
                'Handle': prod.handle,
                'Title': '', 
                'Body (HTML)': '', 
                'Vendor': '', 
                'Type': '', 
                'Tags': '', 
                'Published':'', 
                'Option1 Name':'', 
                'Option1 Value':'', 
                'Option2 Name':'', 
                'Option2 Value':'', 
                'Option3 Name':'', 
                'Option3 Value':'', 
                'Variant SKU':'', 
                'Variant Grams':'', 
                'Variant Inventory Tracker':'', 
                'Variant Inventory Policy':'', 
                'Variant Fulfillment Service':'', 
                'Variant Price': '', 
                'Variant Compare At Price': '', 
                'Variant Requires Shipping': '', 
                'Variant Taxable':'', 
                'Variant Barcode':'', 
                'Image Src': '', 
                'Image Position': '', 
                'Image Alt Text': '', 
                'Gift Card': '', 
                'SEO Title': '', 
                'SEO Description': '', 
                'Google Shopping / Google Product Category': '', 
                'Google Shopping / Gender': '', 
                'Google Shopping / Age Group': '', 
                'Google Shopping / MPN': '', 
                'Google Shopping / AdWords Grouping': '', 
                'Google Shopping / AdWords Labels': '', 
                'Google Shopping / Condition': '', 
                'Google Shopping / Custom Product': '', 
                'Google Shopping / Custom Label 0': '', 
                'Google Shopping / Custom Label 1': '', 
                'Google Shopping / Custom Label 2': '', 
                'Google Shopping / Custom Label 3': '', 
                'Google Shopping / Custom Label 4': '', 
                'Variant Image': '', 
                'Variant Weight Unit': '', 
                'Variant Tax Code': '', 
                'Cost per item': ''
            }
            rows.append(row)
    
    for i in range(len(prod.sku)):
        rows[i]['Variant SKU'] = prod.sku[i]
    for i in range(len(prod.price)):
        rows[i]['Variant Price'] = prod.price[i]
    for i in range(len(prod.oldprice)):
        rows[i]['Variant Compare At Price'] = prod.oldprice[i]
    for i in range(len(prod.barcode)):
        rows[i]['Variant Barcode'] = prod.barcode[i]
    for i in range(len(prod.images)):
        rows[i]['Image Src'], rows[i]['Image Alt Text'] = prod.images[i]
        if rows[i]['Image Src'] != '':
            rows[i]['Image Position'] = i + 1
    
    for i in range(len(prod.sizes)):
        if len(prod.colors) > 1:
            rows[0]['Option2 Name'] = 'Color'
            for j in range(len(prod.colors)):
                rows[i*len(prod.colors)+j]['Option1 Value'] = prod.sizes[i]
                rows[i*len(prod.colors)+j]['Option2 Value'], rows[i*len(prod.colors)+j]['Variant Image']  = prod.colors[j]
                # 
        else:
            rows[i]['Option1 Value'] = prod.sizes[i]
            if len(prod.colors) == 1:
                rows[i]['Option2 Value'], rows[i]['Variant Image'] = prod.colors[0]
                if rows[i]['Option2 Value'] != '' and rows[i]['Option1 Name'] != '':
                    rows[i]['Option2 Name'] = "Color"
    
    # THIS IS WHERE ANY MANIPULATION OF CSV CREATION GOES
    # 
            
    return rows

def getInventory(prod):
    rows = []
    cn = len(prod.colors)
    if cn == 0:
        cn = 1
    cn *= len(prod.sizes)
    for i in range(cn):
        row = {
            'Handle': prod.handle,
            'Title': prod.title, 
            'Option1 Name': 'Size', 
            'Option1 Value':'', 
            'Option2 Name':'', 
            'Option2 Value':'', 
            'Option3 Name':'', 
            'Option3 Value':'', 
            'SKU':'', 
            'Online Brite Creations':'', 
            'Retail Brite Creations':''
        }
        rows.append(row)
    
    for i in range(min(len(rows), len(prod.sku))):
        rows[i]['SKU'] = prod.sku[i]
    for i in range(len(prod.sizes)):
        if len(prod.colors) > 1:
            rows[0]['Option2 Name'] = 'Color'
            for j in range(len(prod.colors)):
                rows[i*len(prod.colors)+j]['Option1 Value'] = prod.sizes[i]
                rows[i*len(prod.colors)+j]['Option2 Value'], b  = prod.colors[j]
                # 
        else:
            rows[i]['Option1 Value'] = prod.sizes[i]
            if len(prod.colors) == 1:
                rows[i]['Option2 Value'], b = prod.colors[0]
                if rows[i]['Option2 Value'] != '' and rows[i]['Option1 Name'] != '':
                    rows[i]['Option2 Name'] = "Color"
    # for r in rows:
    #     if r['SKU'] is not None:
    #         r['Retail Brite Creations'] = 0
    for i in range(len(prod.inventory)):
        rows[i]['Online Brite Creations'] = prod.inventory[i][0]
        rows[i]['Retail Brite Creations'] = prod.inventory[i][1]

    return rows


def productstocsv(products):
    with open('products.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        # fieldnames = ['Collection', 'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value', 'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position', 'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description', 'Google Shopping / Google Product Category', 'Google Shopping / Gender', 'Google Shopping / Age Group', 'Google Shopping / MPN', 'Google Shopping / AdWords Grouping', 'Google Shopping / AdWords Labels', 'Google Shopping / Condition', 'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0', 'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2', 'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4', 'Variant Image', 'Variant Weight Unit', 'Variant Tax Code', 'Cost per item']
        fieldnames = ['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value', 'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position', 'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description', 'Google Shopping / Google Product Category', 'Google Shopping / Gender', 'Google Shopping / Age Group', 'Google Shopping / MPN', 'Google Shopping / AdWords Grouping', 'Google Shopping / AdWords Labels', 'Google Shopping / Condition', 'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0', 'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2', 'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4', 'Variant Image', 'Variant Weight Unit', 'Variant Tax Code', 'Cost per item']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        errors = []
        i = 0
        for p in products:
            try:
                writer.writerows(getrows(p))
                print(i)
                i += 1
            except:
                errors.append(p.title)
        print("Errors: ", end='')
        print(errors)

def productstoinventory(products, multiples=None):
    with open('inventory.csv', 'w', newline='') as csvfile:
        fieldnames = ['Handle', 'Title', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value', 'SKU', 'Online Brite Creations', 'Retail Brite Creations']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in products:
            # try:
            writer.writerows(getInventory(p))
                
                

def instoreinventory(csvname):
    products = []
    multiples = []
    with open(csvname, encoding='utf-8-sig') as vivek:
        reader = csv.DictReader(vivek)
        for row in reader:
            handle = row['handle']
            title = row['title']
            vendor = row['vendor']
            type = row['type']
            price = row['price']
            oldprice = row['oldprice']
            skubase = row['SKU']
            sizes = row['sizes'].replace(' ','').split(',')
            for i in range(len(sizes)):
                if '(' in sizes[i]:
                    multiples.append(skubase + sizes[i][:-3])
                    sizes[i] = sizes[i].replace('(2)', '')
            body = row['description'].replace('\n','').replace(',', '</li>\n<li>')
            body = '<meta charset=\"utf-8\">\n<ul>' + body[5:] + '</li>\n</ul>'
            tags = []
            sku = []
            for s in sizes:
                tags.append('size-' + str(s).replace(' ', ''))
                sku.append(skubase + str(s))
            imgbase = 'https://raw.githubusercontent.com/abadari3/PictureCollector/master/'
            bs = row['images'].split(', ')
            images = []
            for b in bs:
                images.append((imgbase+b+'.png', ''))
            products.append(product(handle=handle, title=title, body=body, vendor=vendor, type=type, tags=tags, sizes=sizes, price=price, oldprice=oldprice, images=images, sku=sku))

    productstocsv(products)
    productstoinventory(products)


def make(row):
    handle = row['Handle'].replace('/', '-')
    title = row['Title']
    body = row['Description']
    vendor = "Mauri"
    type = row['Type']
    sizes = row['Sizes'].split(', ')
    colors = row['Colors'].split(', ')
    images = row['Images'].replace("'", "").split(',')
    colors = [(colors[i], "https://raw.githubusercontent.com/abadari3/Shopify-Product-Manager/master/pics/" + images[0 + i * int(len(images)/len(colors))].strip()) for i in range(len(colors))]
    images = [("https://raw.githubusercontent.com/abadari3/Shopify-Product-Manager/master/pics/" + images[i].strip(), "") for i in range(len(images))]
    tags = []
    for p, i in colors:
        tags.append('color:' + p)
    for s in sizes:
        tags.append('size:' + s)
    sku = []
    j = 0
    for s in sizes:
        for c, i in colors:
            j += 1
            text = handle + "-" + c + "-" + s
            text = text.lower().replace(' ', '').replace('/', '-').replace('.', '-')
            sku.append(text)
    price = []
    for i in range(j):
        price.append(row['Price'])
    # print(sku)
    return product(handle=handle, sku=sku, title=title, body=body, vendor=vendor, type=type, tags=tags, sizes=sizes, colors=colors, price=price, oldprice=price, images=images)
    # return row

def mauri():
    products = []
    with open('mauri.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        # print(reader.fieldnames)
        for row in reader:
            products.append(make(row))

    productstocsv(products)
    productstoinventory(products)

    images = []
    for p in products:
        images.extend([p.images[i][0] for i in range(len(p.images))])
    for i in images:
        result = requests.get(i)
        if result.status_code != 200:
            print(i)
        else:
            print('good')


# mauri()

# prod = csvtoproducts('products.csv')
# colors = {}
# for p in prod:
#     for a, b in p.colors:
#         # print(b)
#         title = a.lower().replace(' ', '-').replace('/', '-').replace('--', '-').replace('--', '-').replace('--', '-')
#         if title not in colors.keys():
#             colors[title] = [b]
#         else:
#             colors[title].append(b)


# # print(colors)
# from swatch import *
# cols = []
# for k in colors.keys():
#     cols.append(k)
#     for i in colors[k]:
#         i = i.replace(' ', '')
#         try:
#             getswatch(k, i)
#         except:
#             print(k, i)


# products = csvtoproducts('products_export_1.csv')
# valid = []
# for p in products:
#     if p.title in ['Bubble', 'Carnage', 'Mustang', 'Player', 'Hawk', 'Floss', 'Jackpot', 'Everglades', 'Casino', 'Apocalypse', 'Hitman', 'Blackjack', 'Flash', 'Rambo', 'Pathfinder', 'Professor', 'Esquire', 'Harlem', 'Vegas', 'Priest', 'Piave', 'Whispers', 'Swag', 'Duke', 'Elegance', 'Steamboat', 'Matrix', 'Predator', 'Opulent', 'High-speed', 'Finesse', 'Stephen', 'Corleone', 'Regal', 'Royalty', 'Boulevard', 'Earth', 'Godfather', 'Cardinal', 'Double Dragon', 'Jurassic', 'Cheetah', 'Black Skin Dress Shoe', 'Brown Tone Dress Boot', 'Prague', 'Belt & Buckle', 'Arno', 'Oglio', 'Symphony', 'Trendsetter', 'Sunset', 'Tide', 'Scenic', 'Luxor', 'Sarasota', 'Romano', 'Cathedral', 'Sandstone']:
#         valid.append(p)
# productstocsv(products)

# prod = csvtoproducts('nocolors.csv')
# colors = []
# for p in prod:
#     cols = []
#     for t in p.tags:
#         if 'color' not in t:
#             if t != '':
#                 cols.append(t)
#     for c, i in p.colors:
#         cols.append('color:' + c)
#     p.tags = cols
# productstocsv(prod)


# prods = csvtoproducts('products_export_1.csv')
# for p in prods:
#     clrs = p.colors
#     colors = []
#     imgvariants = []
#     images = [i for i, a in p.images]
#     for c, i in clrs:
#         colors.append(c)
#         imgvariants.append(i)
#     for ci in range(len(colors)):
#         c = colors[ci]
#         for i in images:
#             if c.replace('/','') in i:
#                 imgvariants[ci] = i

#     fin = []
#     for j in range(len(colors)):
#         fin.append((colors[j], imgvariants[j]))
#     p.colors = fin

# productstocsv(prods)
    # break

# products = csvtoproducts("products_export_1.csv")
# for p in products:
#     v = p.vendor
#     h = p.handle
#     sz = p.sizes
#     c = p.colors
#     sku = p.sku
#     if(p.vendor == "Tiglio"):
#         for s in range(len(sku)):
#             sku[s] = "TIG-"
#             sku[s] += p.title.upper().replace(' ', '').replace('-', '')
#             sku[s] += "-" + sz[(int)(s*len(sz)/len(sku))].upper().replace('/', '-')
#             if len(c) != 1:
#                 sku[s] += "-" + c[(int)(s%len(c))][0].upper().replace(' ', '-').replace('/', '-')
            
#             sku[s] = sku[s].replace('.', '').replace(',', '').replace('\'', '').replace('\"', '').replace('&', '').replace('--', '-')
#         # print(p.sku)
#     else : 
#     # for s in sku:
#     #     print(s)
#         style = ""
#         body = p.body.split('\n')
#         for b in body:
#             if("Style" in b):
#                 style = b
#         if("Style" in style):
#             style = style[style.index("Style"):]
#             style = style[style.index("M"):]
#             style = style[:style.index("<")]
#         for s in range(len(sku)):
#             sku[s] = "WF-" + style + "-" + p.sizes[s]
#     # print()
# productstocsv(products)

