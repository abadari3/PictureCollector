from product import product
from inventory import *
import requests
from bs4 import BeautifulSoup


# instoreinventory('vivekinstore.csv')

def getTitleAndHandle(soup):
    # title = soup.title.text.replace('\n', '').replace('– Carrucci Shoes', '').replace('  ','').replace(',', '')
    # handle = title[:title.index(' ')]
    # title = title[title.index(' ') + 1:]
    # title += '-'
    # title = title[:title.index('-')]
    # title = title.replace('Carrucci ', '')
    title = soup.title.text
    if 'AmbrogioShoes' in title:
        title = title.replace('\n', '')
        # .replace(' – AmbrogioShoes', '').replace('Designer Shoes', '').replace('Men\'s', '').replace('  ',' ').replace('  ',' ').strip()
        title = title[title.index(' '):].strip()
        title = title[title.index(' '):].strip()
        title = title[:title.index(' ')]
    else:
        title = title[title.index(' '):].strip()
        title = title[:title.index(' ')]
    
    handle = title.lower().replace(' ', '')
    return title, handle

def getSizesAndTagsAndColors(soup):
    sizes = []
    # TO DO: GET SIZES FROM WEBSITE
    # print(soup.prettify())
    
    # TO DO add (pairs) of Color string, and its variant image.
    temp1 = []
    one = soup.find_all("div", {"class": "selector-wrapper js product-form__item"})
    label = one[0].find('label').text.replace('\n','').replace(' ','')
    for c in one[0].find_all("option"):
        temp1.append((c.text, ''))
    
    if 'Color' in label:
        colors = temp1
        # print(one[1].find('label').text.replace('\n','').replace(' ',''))
        for c in one[1].find_all("option"):
            sizes.append(c.text)
    else :
        colors = []
        for c in one[0].find_all("option"):
            sizes.append(c.text)
    
    tags = []
    for s in sizes:
        tags.append('size-' + str(s).replace(' ', ''))
    return sizes, tags, colors

def getPrices(soup):
    p = soup.find('span', {'itemprop': 'price'})
    oldprice = p.text.replace('\n','').replace(' ','').replace('$','')
    oldprice = oldprice[:oldprice.index('.')]
    price = str(int(int(oldprice)*0.9))
    # TO DO, GET OLD PRICE FROM WEBSITE
    # CURRENT PRICE IS 10% off
    return price, oldprice

def getImages(soup):
    images = []
    one = soup.find('ul', {'class': 'grid grid--uniform product-single__thumbnails product-single__thumbnails-product-template'})
    if one is None:
        one = soup.find('img', {'class': 'product-featured-img js-zoom-enabled'})
        link = 'https:' + one['src']
        base = link[:link.index('?v')]
        base = base[-4:]
        link = link[:link.index('_530')]
        link += base
        images.append((link, ''))
        return images
    two = one.find_all('a')
    for t in two:
        link = 'https:' + t.find('img')['src']
        base = link[:link.index('?v')]
        base = base[-6:]
        base = base[base.index('.'):]
        link = link[:link.index('_110')]
        link += base
        images.append((link, ''))

    # TO DO add (tuples) of image url, image alt text
    return images

def getDescription(soup):
    description = None
    title, handle = getTitleAndHandle(soup)
    d = soup
    if "AmbrogioShoes" in soup.title.text:
        d  = soup.find('div', {'class': 'ProductMeta__Description Rte'})
    else:
        d = soup.find('div', {'class': 'tr_box'})
    # ps = d.find_all('p')
    desc = d.text.replace('  ', '').split('\n')
    # return desc
    # print(desc)
    descriptions = []
    
    for i in range(len(desc)):
        if not (desc[i] == '' or desc[i] == ' ') and 'Color' not in desc[i] and title.upper() not in desc[i] and 'GUARANTEED' not in desc[i] and 'MaTiSte' not in desc[i] and 'Fennix' not in desc[i] and 'NOTE' not in desc[i] and 'Help?' not in desc[i] and '8UK' not in desc[i]:
            descriptions.append(desc[i])
    descriptions.append("Best Quality, and Price from Brite Creations Atlanta.")
    # TO DO get description from website
    # convert to bullet point list
    descriptions.pop(0)
    if 'Hardware' not in descriptions[0]:
        descriptions.insert(0, 'Hardware: None')
    description = '<meta charset=\"utf-8\">\n<ul>'
    for de in descriptions:
        description += '\n<li>' + de + '</li>'
    description += '\n</ul>'
    return description

def getSKU(handle, colors, sizes):
    skus = []
    # CARRUCI-style code-color-size
    if len(colors) == 0:
        for s in sizes:
            skus.append('CARRUCCI-' + handle + '-' + s)
        return skus
    for c in colors:
        for s in sizes:
            skus.append('CARRUCCI-' + handle + '-' + c.replace(' ', '-') + '-' + s)
    return skus

def getSEO(soup):
    seotitle = None
    seodescription = None
    # TO DO add better titles and descriptions for products
    return seotitle, seodescription

products = []
def createProduct(souplist, type):
    # list of links for this product
    global products
    # vendor = "Carrucci"

    # TO DO STILL
    # sizes, tags, colors = getSizesAndTagsAndColors(souplist[0])         #still have to link variant images
    # images = getImages(souplist[0])

    # DONE
    # title, handle = getTitleAndHandle(souplist[0])
    # price, oldprice = getPrices(souplist[0])
    # sku = getSKU(handle, [a for a, b in colors], sizes)
    # seotitle, seodescription = getSEO(souplist[0])
    body = getDescription(souplist[0])
    # print(body)

    products.append(
        # product(
        #     handle=handle,
        #     title=title, 
        #     body=body, 
        #     vendor=vendor, 
        #     type=type, 
        #     sizes=sizes,
        #     colors=colors, 
        #     price=price, 
        #     oldprice=oldprice, 
        #     images=images, 
        #     seotitle=seotitle, 
        #     seodescription=seodescription, 
        #     sku=sku
        # )
        body
    )
    # here, we have the SOUPs for each product's corresponding links in a list.

# dict of code to list
# where list holds a list of links with that code
linklist = {}
def parselink(soup):
    # title = soup.title.text.replace('\n', '').replace('– Carrucci Shoes', '').replace('  ','').replace(',', '')

    # print(title)
    k, h = getTitleAndHandle(soup)
    global linklist
    if k in linklist.keys():
        linklist[k].append(soup)
    else:
        linklist[k] = [soup]

def main(url): 
    result = requests.get(url)
    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
        # print('Good URL')
    else:
        print(url)
        print('invalid url')
        return
    parselink(soup)

def make(pages, type):
    global linklist
    linklist = {}
    i = 0
    for page in pages:
        # print(i)
        i += 1
        main(page)

    j = 0
    for key in linklist.keys():
        # print(key)
        j += 1
        createProduct(linklist[key], type)
        # print('----------------------------------')



# duca = [
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-amalfi-mens-shoes-black-top-and-white-side-suede-patent-leather-loafers-d4701", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-asti-mens-shoes-black-combination-calf-skin-leather-oxfords-d4706", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-capua-black-velvet-patent-loafers-d4634", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-cassino-yellow-calf-skin-loafers-d4622", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-cecina-mens-designer-shoes-black-calf-skin-leather-cap-toe-oxfords-d4800", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-ferrara-cognac-olive-calf-skin-oxfords-d4627", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-forli-black-calf-skin-loafers-d4604", 
#     "https://www.ambrogioshoes.com/products/duca-imola-mens-shoes-burgundy-alligator-print-leather-sneakers-d4713", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-latina-burgundy-calf-skin-leather-loafers-d4528", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-lucca-blue-calf-skin-loafers-d4615", 
#     "https://www.ambrogioshoes.com/products/duca-maratea-mens-designer-designer-shoes-black-crystal-calf-skin-leather-loafers-d4804", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-marino-bordo-bone-calf-skin-oxfords-d4623", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-milano-brown-cognac-calf-skin-leather-oxfords-d4532", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-napoli-taupe-dark-brown-calf-skin-leather-oxfords-d4538", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-ostia-black-white-calf-skin-oxfords-d4632", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-palermo-blue-combination-calf-skin-leather-boots-d4539", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-parma-chocolate-cognac-snake-print-calf-skin-leather-boots-d4543", 
#     "https://www.ambrogioshoes.com/products/duca-pesaro-mens-designer-designer-shoes-yellow-calf-skin-leather-wing-tip-oxfords-d4806", 
#     "https://www.ambrogioshoes.com/collections/mens-exotic-skin-shoes/products/duca-prato-mens-shoes-black-lizard-snake-print-leather-boots-d4720", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-ravello-black-calf-skin-oxfords-d4628", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-rieti-light-blue-calf-skin-loafers-d4618", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-roma-cognac-purple-calf-skin-leather-oxfords-d4552", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-salerno-cognac-red-snake-print-calf-skin-leather-oxfords-d4554", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-sarno-black-velvet-patent-leather-loafers-d4556", 
#     "https://www.ambrogioshoes.com/products/duca-scala-mens-designer-designer-shoes-black-gold-calf-skin-leather-loafers-d4807", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-siena-black-calf-skin-leather-loafers-d4559", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-sora-black-calf-skin-oxfords-d4610", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-tivoli-cognac-chocolate-calf-skin-oxfords-d4613", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-torino-black-combination-calf-skin-leather-oxfords-d4564", 
#     "https://www.ambrogioshoes.com/products/duca-udine-mens-shoes-black-calf-skin-leather-boots-d4729", 
#     "https://www.ambrogioshoes.com/products/duca-varsi-mens-designer-designer-shoes-navy-alligator-print-calf-skin-leather-sneaker-d4811", 
#     "https://www.ambrogioshoes.com/collections/duca-shoes/products/duca-shoes-mens-venezia-black-velvet-patent-leather-loafers-d4575"
# ]

# # Made in Italy, Emilio Franco shoes have a flawless blend of timeless charm and genuine quality. The brand comes up with new and understated collections every season. It specializes in manufacturing high-quality and premium leather shoes for men.
# emilio = [
#     "https://www.ambrogioshoes.com/collections/emilio-franco-shoes/products/emilio-franco-adamo-mens-shoes-burgundy-calf-skin-leather-oxfords-ef3600", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-amadeo-cognac-calf-skin-leather-oxfords-ef3524", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-angelo-light-blue-combo-calf-skin-leather-oxfords-ef3526", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-antonio-cognac-navy-suede-calf-skin-leather-oxfords-ef3410", 
#     "https://www.ambrogioshoes.com/collections/emilio-franco-shoes/products/emilio-franco-baldo-mens-shoes-antique-red-calf-skin-leather-monkstraps-loafers-ef3602", 
#     "https://www.ambrogioshoes.com/collections/emilio-franco-shoes/products/emilio-franco-ciro-mens-shoes-ash-grey-calf-skin-leather-oxfords-ef3604", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-daniele-brown-combination-suede-loafers-ef3412", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-dante-black-grey-calf-skin-leather-oxfords-ef3518", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-dante-ii-mens-shoes-brown-calf-skin-leather-oxfords-ef3606", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-davide-brandy-calf-skin-leather-boots-ef3414", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-diego-navy-suede-oxfords-ef3417", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-dino-mens-shoes-navy-calf-skin-leather-oxfords-ef3612?variant=30808020287626", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-eduardo-yellow-combo-calf-skin-leather-oxfords-ef3523", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-francesco-black-suede-loafers-ef3418", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-franco-navy-calf-skin-leather-oxfords-ef3427", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-gino-black-white-calf-skin-leather-oxfords-ef3500", 
#     "https://www.ambrogioshoes.com/collections/mens-shoes/products/emilio-franco-shoes-mens-giorgio-grey-calf-skin-leather-oxfords-ef3429", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-leonardo-black-suede-boots-ef3436", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-lorenzo-mens-shoes-bone-and-brown-calf-skin-leather-oxfords-ef3618", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-luca-black-calf-skin-leather-loafers-ef3439",  
#     "https://www.ambrogioshoes.com/products/emilio-franco-luico-mens-shoes-black-combination-snake-print-and-calf-skin-leather-boots-ef3619", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-luigi-black-calf-skin-leather-oxfords-ef3441", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-marco-grey-combination-calf-skin-leather-oxfords-ef3445", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-marino-taupe-black-calf-skin-leather-oxfords-ef3506", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-martino-mens-shoes-brown-combination-snake-print-and-calf-skin-leather-oxfords-ef3621", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-milo-mens-shoes-brown-calf-skin-leather-boots-ef3624", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-nico-mens-shoes-navy-calf-skin-leather-oxfords-ef3626", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-oliviero-mens-shoes-olive-suede-leather-loafers-ef3628", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-piero-mens-shoes-navy-suede-leather-loafers-ef3630", 
#     "https://www.ambrogioshoes.com/collections/mens-shoes-under-300/products/emilio-franco-pietro-mens-shoes-antique-red-and-burgundy-calf-skin-leather-oxfords-ef3631", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-remo-mens-shoes-black-and-grey-texture-print-and-calf-skin-leather-boots-ef3633", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-renato-black-patent-leather-oxfords-ef3515", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-riccardo-mens-shoes-black-calf-skin-leather-loafers-ef3635", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-sandro-cognac-calf-skin-leather-oxfords-ef3513", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-mens-shoes-black-and-grey-suede-leather-loafers-ef3638", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-shoes-mens-stefano-wine-calf-skin-leather-oxfords-ef3457", 
#     "https://www.ambrogioshoes.com/products/emilio-franco-dario-mens-shoes-cognac-and-brown-calf-skin-leather-chelsea-boots-ef3609"
# ]

# fennix = [
#     "https://www.dellamoda.com/Fennix-3044-Men-s-Italian-Black-Hornback-and-Calf-Skin-Sneakers-FX2353.html", 
#     "https://www.dellamoda.com/Fennix-Men-s-Italian-Shoes-Navy-Oxfords-FX2115.html", 
#     "https://www.dellamoda.com/Fennix-Adam-Men-s-Italian-Blue-Alligator-Sneakers-FX2301.html", 
#     "https://www.dellamoda.com/Fennix-Alex-Men-s-Shoes-Black-Alligator-and-Deer-Skin-Leather-Sneakers-FX2400.html", 
#     "https://www.dellamoda.com/Fennix-Arthur-Men-s-Italian-Navy-and-Red-Calf-skin-Leather-and-Alligator-Oxfords-FX2305.html", 
#     "https://www.dellamoda.com/Fennix-Charlie-Men-s-Shoes-Dark-and-Light-Grey-Genuine-Eel-Skin-Leather-Oxfords-FX2403.html", 
#     "https://www.dellamoda.com/Fennix-Ethan-Men-s-Shoes-Cognac-Alligator-and-Calf-Skin-Leather-Oxfords-FX2404.html", 
#     "https://www.dellamoda.com/Fennix-Finley-Men-s-Italian-Black-Calf-skin-Leather-and-Crocodile-Oxfords-FX2308.html", 
#     "https://www.dellamoda.com/Fennix-George-Men-s-Italian-Burgundy-Velvet-and-Alligator-Loafers-FX2311.html", 
#     "https://www.dellamoda.com/Fennix-Harry-Men-s-Shoes-Black-Ostrich-and-Suede-Leather-Loafers-FX2407.html", 
#     "https://www.dellamoda.com/Fennix-Hugo-Men-s-Italian-Cognac-Hornback-Alligator-Oxfords-FX2315.html", 
#     "https://www.dellamoda.com/Fennix-Jack-Men-s-Italian-Red-Hornback-Crocodile-and-Calf-skin-Leather-Sneakers-FX2321.html", 
#     "https://www.dellamoda.com/Fennix-Jacob-Men-s-Shoes-Black-Alligator-and-Lizard-Skin-Loafers-FX2410-Fennix-Jacob-Men-s-Shoes-Black-Alligator-and-Lizard-Skin-Loafers-FX2410.html", 
#     "https://www.dellamoda.com/Fennix-Jake-Men-s-Italian-Black-Alligator-and-Calf-skin-Leather-Sneakers-FX2322.html", 
#     "https://www.dellamoda.com/Fennix-James-Men-s-Italian-Pink-Alligator-and-Suede-Oxfords-FX2329.html", 
#     "https://www.ambrogioshoes.com/products/fennix-miles-mens-italian-bordo-burgundy-exotic-alligator-wingtip-oxfords-fx2506", 
#     "https://www.dellamoda.com/Fennix-Oliver-Men-s-Italian-Red-Alligator-Oxfords-FX2346.html", 
#     "https://www.dellamoda.com/Fennix-Oscar-Men-s-Shoes-Black-and-White-Genuine-Eel-Skin-Loafers-FX2413.html", 
#     "https://www.dellamoda.com/Fennix-Theo-Men-s-Italian-Pink-Alligator-and-Calf-Skin-Oxfords-FX2350.html", 
#     "https://www.dellamoda.com/Fennix-Tyler-Men-s-Shoes-Anitque-Red-Alligator-and-Calf-Skin-Leather-Oxfords-FX2419.html"
# ]

# # prds = csvtoproducts('fennix.csv')

# # # for p in prds:
# # #     print(p.vendor + " - " + p.title)

# # make(fennix, "Dress Shoes")

# # for p in range(len(products)):
# #     prds[p].body = products[p]
# #     print(prds[p].title)
# #     # print(products[p])
# #     # print('----------------------------------')

# # sku = []
# # for p in prds:
# #     for s in p.sizes:
# #         for c, i in p.colors:
# #             sku.append(p.handle + "-" + c.replace(' ', '').lower() + "-" + str(s).replace('.0', '').replace('.5', '5'))
# #             p.sku = sku
# #     sku = []

# # productstocsv(prds)
# # productstoinventory(prds)

# products = csvtoproducts('products.csv')
# cs = {}
# for p in products:
#     for c, i in p.colors:
#         # c = c.lower().replace(' ', '-').replace('.', '')
#         if i == '':
#             break
#         if c in cs.keys():
#             cs[c].append(i)
#         else:
#             cs[c] = [i]

# from swatch import *

# cols = []
# for k in cs.keys():
#     cols.append(k)
#     for i in cs[k]:
#         # getswatch(k, i)
#         print(k, i)

# # cols.sort()
# # for c in cols:
# #     print(c)
# # print(len(cs.keys()))


# # also add "https://www.carrucci.com/collections/all/products/carrucci-leather-belt" later
# # dressshoes = [
# #     "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-02p-carrucci-shoes", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-102v-carrucci-velvet-loafer", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-210sp-carrucci-formal-dress-shoes-with-bow-navy-black", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-210sp-carrucci-formal-dress-shoes-with-bow-black", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-210sp-carrucci-poem-shoes-with-bow-red", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-103v-velvet-prom-loafer-gray", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-103v-velvet-prom-loafer-emerald", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-103v-velvet-prom-loafer-red", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-103v-velvet-prom-loafer-black", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks308-101v-velvet-buckle-loafer-black", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks308-101v-velvet-buckle-loafer-navy", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks308-101v-velvet-buckle-loafer-burgundy", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks805-05sg-suede-studs-loafer-black", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks805-10ss-carrucci-studs-loafer-burgundy", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks805-10ss-carrucci-studs-loafer-black", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-102v-carrucci-velvet-prom-loafer-gray", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-102v-carrucci-velvet-prom-loafer-black", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-102v-carrucci-velvet-prom-loafer-emerald", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-102v-carrucci-velvet-prom-loafer-navy", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-01p-carrucci-shoes", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks308-01-carrucci-burgundy-velvet-loafer", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks475-02p-carrucci-prom-loafer", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks308-08b2-buckle-loafer-black-suede", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks308-08b2-buckle-loafer-brown-suede", 
# #     "https://www.carrucci.com/collections/formal-dress-shoes/products/ks308-08b2-buckle-loafer-navy-suede", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks805-05sg-suede-studs-dress-shoes-burgundy", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks308-08b2-buckle-loafer-red-suede", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks805-05sg-suede-studs-dress-shoes-navy", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks805-05sg-suede-studs-dress-shoes-red", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks805-05sg-suede-studs-dress-shoes-bone", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks805-07sv-carrucci-hand-embroidered-bling-dress-shoes-sapphire", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks805-07sv-carrucci-hand-embroidered-bling-dress-shoes-rose-gold", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-210n-carrucci-formal-dress-shoes", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-210n-carrucci-formal-dress-shoes-1", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-210n-carrucci-formal-dress-shoes-2", "https://www.carrucci.com/collections/formal-dress-shoes/products/ks525-102p-carrucci-patent-leather-bow-tie-dress-shoes"
# # ]
# # make(dressshoes, "Dress Shoe")

# # loafers = [
# #     "https://www.carrucci.com/collections/loafers/products/ks525-305-soft-leather-casual-buckle-loafer-mule-1", "https://www.carrucci.com/collections/loafers/products/ks525-305-soft-leather-casual-buckle-loafer-mule", "https://www.carrucci.com/collections/loafers/products/ks515-03-whole-cut-leather-loafer-3", "https://www.carrucci.com/collections/loafers/products/ks509-23-double-monk-straps-leather-shoes-2", "https://www.carrucci.com/collections/loafers/products/ks515-03-whole-cut-leather-loafer-2", "https://www.carrucci.com/collections/loafers/products/ks515-03-whole-cut-leather-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks515-03-whole-cut-leather-loafer", "https://www.carrucci.com/collections/loafers/products/ks509-23-double-monk-straps-leather-shoes-1", "https://www.carrucci.com/collections/loafers/products/ks509-23-double-monk-straps-leather-shoes", "https://www.carrucci.com/collections/loafers/products/ks478-120sc-patina-finish-leather-penny-loafer-2", "https://www.carrucci.com/collections/loafers/products/ks478-120sc-patina-finish-leather-penny-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks478-120sc-patina-finish-leather-penny-loafer", "https://www.carrucci.com/collections/loafers/products/ks478-119s-suede-penny-loafer-w-leather-trim-5", "https://www.carrucci.com/collections/loafers/products/ks478-119s-suede-penny-loafer-w-leather-trim-4", "https://www.carrucci.com/collections/loafers/products/ks478-119s-suede-penny-loafer-w-leather-trim-3", "https://www.carrucci.com/collections/loafers/products/ks478-119s-suede-penny-loafer-w-leather-trim-2", "https://www.carrucci.com/collections/loafers/products/ks478-119s-suede-penny-loafer-w-leather-trim-1", "https://www.carrucci.com/collections/loafers/products/ks478-119s-suede-penny-loafer-w-leather-trim", "https://www.carrucci.com/collections/loafers/products/ks503-60-carrucci-cross-strap-leather-loafer-3", "https://www.carrucci.com/collections/loafers/products/ks503-60-carrucci-cross-strap-leather-loafer-2", "https://www.carrucci.com/collections/loafers/products/ks503-60-carrucci-cross-strap-leather-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks503-60-carrucci-cross-strap-leather-loafer", "https://www.carrucci.com/collections/loafers/products/ks500-12-woven-cap-toe-tassel-loafer", "https://www.carrucci.com/collections/loafers/products/ks503-35-carrucci-buckle-monk-strap-1", 
# #     "https://www.carrucci.com/collections/loafers/products/ks503-35-carrucci-buckle-monk-strap", "https://www.carrucci.com/collections/loafers/products/ks503-02-carrucci-signature-buckle-loafer", "https://www.carrucci.com/collections/loafers/products/ks478-503-carrucci-leather-penny-loafer-7", "https://www.carrucci.com/collections/loafers/products/ks478-118s-leather-suede-penny-loafer-5", "https://www.carrucci.com/collections/loafers/products/ks478-118s-leather-suede-penny-loafer-4", "https://www.carrucci.com/collections/loafers/products/ks478-118s-leather-suede-penny-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks478-118s-leather-suede-penny-loafer-3", "https://www.carrucci.com/collections/loafers/products/ks478-118s-leather-suede-penny-loafer-2", "https://www.carrucci.com/collections/loafers/products/ks478-118s-leather-suede-penny-loafer", "https://www.carrucci.com/collections/loafers/products/ks478-503-carrucci-leather-penny-loafer-6", "https://www.carrucci.com/collections/loafers/products/ks478-503-carrucci-leather-penny-loafer-5", "https://www.carrucci.com/collections/loafers/products/ks478-503-carrucci-leather-penny-loafer-4", "https://www.carrucci.com/collections/loafers/products/ks478-503-carrucci-leather-penny-loafer-3", "https://www.carrucci.com/collections/loafers/products/ks478-503-carrucci-leather-penny-loafer-2", "https://www.carrucci.com/collections/loafers/products/ks478-503-carrucci-leather-penny-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks478-503-carrucci-leather-penny-loafer", "https://www.carrucci.com/collections/loafers/products/ks525-302x-carrucci-chain-buckle-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks708-05-carrucci-calfskin-woven-tassel-loafers-2", "https://www.carrucci.com/collections/loafers/products/ks708-05-carrucci-calfskin-woven-tassel-loafers-1", "https://www.carrucci.com/collections/loafers/products/ks708-05-carrucci-calfskin-woven-tassel-loafers", "https://www.carrucci.com/collections/loafers/products/ks478-114e-carrucci-embossed-calfskin-loafer-2", "https://www.carrucci.com/collections/loafers/products/ks478-114e-carrucci-embossed-calfskin-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks478-114e-carrucci-embossed-calfskin-loafer", "https://www.carrucci.com/collections/loafers/products/ks503-47-carrucci-wholecut-tassel-loafer-2", 
# #     "https://www.carrucci.com/collections/loafers/products/ks503-47-carrucci-wholecut-tassel-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks525-102p-carrucci-patent-leather-bow-tie-dress-shoes", "https://www.carrucci.com/collections/loafers/products/victor-timeless-buckle-loafer-in-leather-sole-1", "https://www.carrucci.com/collections/loafers/products/victor-timeless-buckle-loafer-in-leather-sole", "https://www.carrucci.com/collections/loafers/products/ks525-210n-carrucci-formal-dress-shoes-2", "https://www.carrucci.com/collections/loafers/products/ks525-210n-carrucci-formal-dress-shoes-1", "https://www.carrucci.com/collections/loafers/products/ks525-210n-carrucci-formal-dress-shoes", "https://www.carrucci.com/collections/loafers/products/ks525-302x-carrucci-chain-buckle-loafer", "https://www.carrucci.com/collections/loafers/products/ks886-22-carrucci-wingtip-buckle-loafer-2", "https://www.carrucci.com/collections/loafers/products/ks886-22-carrucci-wingtip-buckle-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks886-22-carrucci-wingtip-buckle-loafer", "https://www.carrucci.com/collections/loafers/products/ks479-06-carrucci-moc-toe-buckle-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks479-06-carrucci-moc-toe-buckle-loafer", "https://www.carrucci.com/collections/loafers/products/ks479-06-carrucci-apron-buckle-loafer", "https://www.carrucci.com/collections/loafers/products/ks503-47-carrucci-wholecut-tassel-loafer", "https://www.carrucci.com/collections/loafers/products/ks708-01-carrucci-timeless-tassel-loafer-2", "https://www.carrucci.com/collections/loafers/products/ks708-01-carrucci-timeless-tassel-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks708-01-carrucci-timeless-tassel-loafer", "https://www.carrucci.com/collections/loafers/products/ks478-110e-carrucci-burnished-woven-penny-loafer-3", "https://www.carrucci.com/collections/loafers/products/ks478-110e-carrucci-burnished-woven-penny-loafer-2", "https://www.carrucci.com/collections/loafers/products/ks099-3005ls-carrucci-buckle-loafer", "https://www.carrucci.com/collections/loafers/products/ks478-110e-carrucci-burnished-woven-penny-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks478-110e-carrucci-burnished-woven-penny-loafer", "https://www.carrucci.com/collections/loafers/products/ks708-02-carrucci-timeless-buckle-loafer-2", 
# #     "https://www.carrucci.com/collections/loafers/products/ks708-02-carrucci-timeless-buckle-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks708-02-carrucci-timeless-buckle-loafer", "https://www.carrucci.com/collections/loafers/products/ks503-40-carrucci-modern-penny-loafer-4", "https://www.carrucci.com/collections/loafers/products/ks506-16-carrucci-slip-on-loafer-with-decorative-lace-up", "https://www.carrucci.com/collections/loafers/products/ks503-40-carrucci-modern-penny-loafer-3", "https://www.carrucci.com/collections/loafers/products/ks503-40-carrucci-modern-penny-loafer-2", "https://www.carrucci.com/collections/loafers/products/ks503-40-carrucci-modern-penny-loafer-1", "https://www.carrucci.com/collections/loafers/products/ks503-40-carrucci-modern-penny-loafer", "https://www.carrucci.com/collections/loafers/products/ks478-35-ks503-35-carrucci-burnished-monk-strap", "https://www.carrucci.com/collections/loafers/products/ks099-722-woven-buckle-loafer-brown", "https://www.carrucci.com/collections/loafers/products/ks099-722-woven-buckle-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks099-714-leather-tassel-loafer-patent-leather", "https://www.carrucci.com/collections/loafers/products/ks099-714-leather-tassel-loafer-cognac", "https://www.carrucci.com/collections/loafers/products/ks099-714-leather-tassel-loafer-navy", "https://www.carrucci.com/collections/loafers/products/ks099-710-wingtip-monk-strap-loafer-black-burg", "https://www.carrucci.com/collections/loafers/products/ks099-710-wingtip-monk-strap-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks099-710-wingtip-monk-strap-loafer-brown-cognac", "https://www.carrucci.com/collections/loafers/products/ks099-710-wingtip-monk-strap-loafer-navy", "https://www.carrucci.com/collections/loafers/products/ks099-710-wingtip-monk-strap-loafer-brown-navy", "https://www.carrucci.com/collections/loafers/products/ks099-303t-wingtip-double-monk-straps-brown-cognac", "https://www.carrucci.com/collections/loafers/products/ks099-303t-wingtip-double-monk-straps-black", "https://www.carrucci.com/collections/loafers/products/ks099-303t-wingtip-double-monk-straps-brown-navy-1", "https://www.carrucci.com/collections/loafers/products/ks099-302-cap-toe-double-monk-strap-black", "https://www.carrucci.com/collections/loafers/products/ks099-302-cap-toe-double-monk-strap-whisky", 
# #     "https://www.carrucci.com/collections/loafers/products/ks099-3003-carrucci-double-monkstraps-black-black-patent", "https://www.carrucci.com/collections/loafers/products/ks099-3003-carrucci-double-monkstraps-navy", "https://www.carrucci.com/collections/loafers/products/ks099-3003-carrucci-double-monkstraps-oxblood", "https://www.carrucci.com/collections/loafers/products/ks099-3003-carrucci-double-monkstraps-black-white", "https://www.carrucci.com/collections/loafers/products/ks099-3003-carrucci-double-monk-straps-cognac", "https://www.carrucci.com/collections/loafers/products/ks1377-12sc-patent-leather-loafer-purple", "https://www.carrucci.com/collections/loafers/products/ks1377-12sc-patent-leather-loafer-burgundy", "https://www.carrucci.com/collections/loafers/products/ks479-05-carrucci-monk-strap-color-loafer-cognac-navy", "https://www.carrucci.com/collections/loafers/products/ks479-05-carrucci-buckle-loafer", "https://www.carrucci.com/collections/loafers/products/ks524-16sc-double-monk-strap-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks524-16sc-double-monk-strap-loafer-brown", "https://www.carrucci.com/collections/loafers/products/ks524-16sc-double-monk-strap-loafer", "https://www.carrucci.com/collections/loafers/products/ks502-03-carrucci-buckle-slip-on-loafer-jade", "https://www.carrucci.com/collections/loafers/products/ks502-03-carrucci-buckle-slip-on-loafer-navy", "https://www.carrucci.com/collections/loafers/products/ks099-812e-carrucci-leather-loafer-coffee", "https://www.carrucci.com/collections/loafers/products/ks099-812e-carrucci-leather-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks2019-15-carrucci-double-buckles-loafer-cognac", "https://www.carrucci.com/collections/loafers/products/ks2019-15-carrucci-double-buckles-loafer-gray", "https://www.carrucci.com/collections/loafers/products/ks2024-04s-carrucci-suede-loafer", "https://www.carrucci.com/collections/loafers/products/ks099-725-carrucci-embossed-leather-and-suede-slip-on", "https://www.carrucci.com/collections/loafers/products/ks2240-05-deerskin-leather-loafer-gray", "https://www.carrucci.com/collections/loafers/products/ks2240-05-deerskin-leather-loafer-burgundy", "https://www.carrucci.com/collections/loafers/products/ks2240-01s-carrucci-leather-suede-slip-on-brown", "https://www.carrucci.com/collections/loafers/products/ks2240-01s-carrucci-leather-suede-slip-on-black", 
# #     "https://www.carrucci.com/collections/loafers/products/ks2240-01s-carrucci-leather-suede-slip-on", "https://www.carrucci.com/collections/loafers/products/ks2240-04-carrucci-deer-skin-monk-strap-slip-on", "https://www.carrucci.com/collections/loafers/products/ks2240-04p-carrucci-deer-skin-patent-leather-slip-on", "https://www.carrucci.com/collections/loafers/products/ks506-16-carrucci-slip-on-loafer-with-decorative-lace-up-navy", "https://www.carrucci.com/collections/loafers/products/ks506-16-carrucci-slip-on-loafer-with-decorative-lace-up-cognac", "https://www.carrucci.com/collections/loafers/products/ks805-07sv-carrucci-hand-embroidered-bling-dress-shoes-sapphire", "https://www.carrucci.com/collections/loafers/products/ks805-07sv-carrucci-hand-embroidered-bling-dress-shoes-rose-gold", "https://www.carrucci.com/collections/loafers/products/ks2240-12t-carrucci-two-tone-penny-loafers-brown-bone-1", "https://www.carrucci.com/collections/loafers/products/ks2240-12t-carrucci-two-tone-penny-loafers-navy-white", "https://www.carrucci.com/collections/loafers/products/ks2240-12t-carrucci-two-tone-penny-loafers-black", "https://www.carrucci.com/collections/loafers/products/ks805-05sg-suede-studs-dress-shoes-bone", "https://www.carrucci.com/collections/loafers/products/ks805-05sg-suede-studs-dress-shoes-red", "https://www.carrucci.com/collections/loafers/products/ks805-05sg-suede-studs-dress-shoes-navy", "https://www.carrucci.com/collections/loafers/products/ks805-05sg-suede-studs-dress-shoes-burgundy", "https://www.carrucci.com/collections/loafers/products/ks478-01-leather-sole-buckle-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks2240-12cc-carrucci-denim-leather-loafer", "https://www.carrucci.com/collections/loafers/products/ks479-609-carrucci-leather-loafer-navy", "https://www.carrucci.com/collections/loafers/products/ks479-609-carrucci-leather-loafer-cognac", "https://www.carrucci.com/collections/loafers/products/ks479-609-carrucci-leather-loafer-burgundy", "https://www.carrucci.com/collections/loafers/products/ks479-609-carrucci-leather-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks503-37-carrucci-double-monk-strap-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks503-39-buckle-leather-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks503-39-buckle-leather-loafer-grey", "https://www.carrucci.com/collections/loafers/products/ks503-39-buckle-leather-loafer-cognac", 
# #     "https://www.carrucci.com/collections/loafers/products/ks525-210sp-carrucci-formal-dress-shoes-with-bow-navy-black", "https://www.carrucci.com/collections/loafers/products/ks525-210sp-carrucci-formal-dress-shoes-with-bow-black", "https://www.carrucci.com/collections/loafers/products/ks525-210sp-carrucci-poem-shoes-with-bow-red", "https://www.carrucci.com/collections/loafers/products/ks503-37-carrucci-double-monk-strap-loafer-cognac", "https://www.carrucci.com/collections/loafers/products/ks503-37-carrucci-double-monk-strap-loafer-navy", "https://www.carrucci.com/collections/loafers/products/ks1170-01-comfort-leather-loafer-black", "https://www.carrucci.com/collections/loafers/products/copy-of-ks1140-03s-leather-strap-suede-loafer", "https://www.carrucci.com/collections/loafers/products/ks478-32-whole-cut-burnished-buckle-loafer-brown", "https://www.carrucci.com/collections/loafers/products/ks478-32-whole-cut-burnished-buckle-loafer-gray", "https://www.carrucci.com/collections/loafers/products/ks478-32-whole-cut-burnished-buckle-loafer-cognac", "https://www.carrucci.com/collections/loafers/products/ks211-385-leather-loafer-navy", "https://www.carrucci.com/collections/loafers/products/ks478-01-leather-sole-buckle-loafer-cognac", "https://www.carrucci.com/collections/loafers/products/ks2240-101-leather-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks2240-101-leather-loafer-white", "https://www.carrucci.com/collections/loafers/products/ks2240-101-leather-loafer-tan", "https://www.carrucci.com/collections/loafers/products/ks099-714-leather-tassel-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks099-307t-two-tone-burnished-monk-strap-brown-cognac", "https://www.carrucci.com/collections/loafers/products/ks099-307t-two-tone-burnished-monk-strap-brown-navy", "https://www.carrucci.com/collections/loafers/products/ks099-307t-two-tone-burnished-monk-strap-oxblood-burgundy", "https://www.carrucci.com/collections/loafers/products/ks099-3003-carrucci-double-monk-straps-black", "https://www.carrucci.com/collections/loafers/products/ks099-722-woven-buckle-loafer-brown-navy", "https://www.carrucci.com/collections/loafers/products/ks525-103v-velvet-prom-loafer-gray", "https://www.carrucci.com/collections/loafers/products/ks525-103v-velvet-prom-loafer-emerald", "https://www.carrucci.com/collections/loafers/products/ks525-103v-velvet-prom-loafer-red", 
# #     "https://www.carrucci.com/collections/loafers/products/ks525-103v-velvet-prom-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks099-725c-buckle-perforated-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks099-725c-buckle-perforated-loafer-brown", "https://www.carrucci.com/collections/loafers/products/ks511-12m-match-bottom-edge-slip-on-loafer-grey", "https://www.carrucci.com/collections/loafers/products/ks511-12m-match-bottom-edge-slip-on-loafer-cobalt", "https://www.carrucci.com/collections/loafers/products/ks511-12m-match-bottom-edge-slip-on-loafer-purple", "https://www.carrucci.com/collections/loafers/products/ks511-12m-match-bottom-edge-slip-on-loafer-olive", "https://www.carrucci.com/collections/loafers/products/ks511-12m-match-bottom-edge-slip-on-loafer-cognac", "https://www.carrucci.com/collections/loafers/products/ks511-12m-match-bottom-edge-slip-on-loafer-burgundy", "https://www.carrucci.com/collections/loafers/products/ks308-101v-velvet-buckle-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks308-101v-velvet-buckle-loafer-navy", "https://www.carrucci.com/collections/loafers/products/ks308-101v-velvet-buckle-loafer-burgundy", "https://www.carrucci.com/collections/loafers/products/ks805-05sg-suede-studs-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks479-607-monk-strap-loafer-cognac", "https://www.carrucci.com/collections/loafers/products/ks479-602-buckle-loafer-burgundy", "https://www.carrucci.com/collections/loafers/products/ks479-602-buckle-loafer-cognac", "https://www.carrucci.com/collections/loafers/products/ks1377-05-contrast-tassel-loafer-navy-white", "https://www.carrucci.com/collections/loafers/products/ks1377-05-contrast-tassel-loafer-navy-red", "https://www.carrucci.com/collections/loafers/products/ks1377-05-contrast-tassel-loafer-brown-navy", "https://www.carrucci.com/collections/loafers/products/ks1377-05-contrast-tassel-loafer-black-white", "https://www.carrucci.com/collections/loafers/products/ks1377-05-contrast-tassel-loafer-black-red", "https://www.carrucci.com/collections/loafers/products/ks261-04-wholecut-two-tone-buckle-loafer-lawn-tan", "https://www.carrucci.com/collections/loafers/products/ks261-04-wholecut-two-tone-buckle-loafer-blue-tan", "https://www.carrucci.com/collections/loafers/products/ks261-04-wholecut-two-tone-buckle-loafer-navy", 
# #     "https://www.carrucci.com/collections/loafers/products/ks1377-06h-pony-loafer-zebra", "https://www.carrucci.com/collections/loafers/products/ks1377-06p-patent-leather-loafer-navy", "https://www.carrucci.com/collections/loafers/products/ks805-10ss-carrucci-studs-loafer-burgundy", "https://www.carrucci.com/collections/loafers/products/ks805-10ss-carrucci-studs-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks503-21sl-suede-loafer-w-leather-trim-burgundy", "https://www.carrucci.com/collections/loafers/products/ks503-21sl-suede-loafer-w-leather-trim-denim", "https://www.carrucci.com/collections/loafers/products/ks261-02-two-tone-leather-loafer-navy", "https://www.carrucci.com/collections/loafers/products/ks261-02-two-tone-leather-loafer-black-burg", "https://www.carrucci.com/collections/loafers/products/ks261-02-two-tone-leather-loafer-blue-tan", "https://www.carrucci.com/collections/loafers/products/ks261-03-two-tone-monk-strap-loafer-lawn-tan", "https://www.carrucci.com/collections/loafers/products/ks261-03-two-tone-monk-strap-loafer-blue-tan", "https://www.carrucci.com/collections/loafers/products/ks261-03-two-tone-monk-strap-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks261-03-two-tone-monk-strap-loafer-blk-burg", "https://www.carrucci.com/collections/loafers/products/ks099-711-embossed-leather-loafer-brown", "https://www.carrucci.com/collections/loafers/products/ks478-35-ks503-35-carrucci-burnished-monk-strap-cognac", "https://www.carrucci.com/collections/loafers/products/ks478-35-ks503-35-carrucci-burnished-monk-strap-chestnut", "https://www.carrucci.com/collections/loafers/products/ks478-35-ks503-35-carrucci-burnished-monk-strap-ocean-blue", "https://www.carrucci.com/collections/loafers/products/ks478-35-ks503-35-carrucci-burnished-monk-strap-black", "https://www.carrucci.com/collections/loafers/products/ks308-08b2-buckle-loafer-brown-suede", "https://www.carrucci.com/collections/loafers/products/ks308-08b2-buckle-loafer-blue", "https://www.carrucci.com/collections/loafers/products/ks308-08b2-buckle-loafer-tan", "https://www.carrucci.com/collections/loafers/products/ks308-08b2-buckle-loafer-black-suede", "https://www.carrucci.com/collections/loafers/products/ks308-08b2-buckle-loafer-red-suede", "https://www.carrucci.com/collections/loafers/products/ks308-08b2-buckle-loafer-navy-suede", 
#     "https://www.carrucci.com/collections/loafers/products/ks308-01-carrucci-burgundy-velvet-loafer", "https://www.carrucci.com/collections/loafers/products/ks308-01-tassel-loafer-charcoal", "https://www.carrucci.com/collections/loafers/products/ks308-01-tassel-loafer-tan", "https://www.carrucci.com/collections/loafers/products/ks308-02s-suede-tassel-loafer-purple", "https://www.carrucci.com/collections/loafers/products/ks308-02s-suede-tassel-loafer-brown", "https://www.carrucci.com/collections/loafers/products/ks308-04-carrucci-tassel-loafer-brown", "https://www.carrucci.com/collections/loafers/products/ks308-04-carrucci-tassel-loafer-black-suede", "https://www.carrucci.com/collections/loafers/products/ks308-04-carrucci-tassel-loafer-charcoal", "https://www.carrucci.com/collections/loafers/products/ks308-07-carrucci-black-calfskin-loafer", "https://www.carrucci.com/collections/loafers/products/ks308-06-perforated-double-monk-strap-coral", "https://www.carrucci.com/collections/loafers/products/ks308-06-perforated-double-monk-strap-brown", "https://www.carrucci.com/collections/loafers/products/ks478-02-carrucci-signature-buckle-loafer-gray", "https://www.carrucci.com/collections/loafers/products/ks478-02-carrucci-signature-buckle-loafer-olive", "https://www.carrucci.com/collections/loafers/products/ks478-02-carrucci-signature-buckle-loafer-cognac", "https://www.carrucci.com/collections/loafers/products/ks478-02-carrucci-signature-buckle-loafer-red", "https://www.carrucci.com/collections/loafers/products/ks478-02-carrucci-signature-buckle-loafer-chestnut", "https://www.carrucci.com/collections/loafers/products/ks478-02-carrucci-signature-buckle-loafer-purple", "https://www.carrucci.com/collections/loafers/products/ks625-101v-velvet-buckle-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks525-102v-carrucci-velvet-prom-loafer-gray", "https://www.carrucci.com/collections/loafers/products/ks525-102v-carrucci-velvet-prom-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks525-102v-carrucci-velvet-prom-loafer-emerald", "https://www.carrucci.com/collections/loafers/products/ks525-102v-carrucci-velvet-prom-loafer-navy", "https://www.carrucci.com/collections/loafers/products/ks524-12-button-up-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks524-12-button-up-loafer-cognac", 
#     "https://www.carrucci.com/collections/loafers/products/ks503-35-monk-strap-loafer-gray", "https://www.carrucci.com/collections/loafers/products/ks503-21sl-suede-loafer-w-leather-trim-gray", "https://www.carrucci.com/collections/loafers/products/ks502-11-double-monk-straps-loafer-gray", "https://www.carrucci.com/collections/loafers/products/ks502-11-double-monk-straps-loafer-chestnut", "https://www.carrucci.com/collections/loafers/products/ks502-11-double-monk-straps-loafer-cognac", "https://www.carrucci.com/collections/loafers/products/ks502-11-double-monk-straps-loafer-cobalt-blue", "https://www.carrucci.com/collections/loafers/products/ks479-602-buckle-loafer-whisky", "https://www.carrucci.com/collections/loafers/products/ks478-501-color-loafer-olive", "https://www.carrucci.com/collections/loafers/products/ks478-501-color-loafer-dk-red", "https://www.carrucci.com/collections/loafers/products/ks478-501-color-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks478-501-color-loafer-blue", "https://www.carrucci.com/collections/loafers/products/ks308-08b2-buckle-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks308-06-perforated-double-monk-strap-black", "https://www.carrucci.com/collections/loafers/products/ks308-02s-suede-tassel-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks259-310-leather-loafer-patent", "https://www.carrucci.com/collections/loafers/products/ks259-310-leather-loafer-brown", "https://www.carrucci.com/collections/loafers/products/ks2240-05-deerskin-leather-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks1377-12sc-patent-leather-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks1377-06h-pony-loafer-brown", "https://www.carrucci.com/collections/loafers/products/ks1377-05-contrast-tassel-loafer-brown-white", "https://www.carrucci.com/collections/loafers/products/ks099-711-embossed-leather-loafer-black", "https://www.carrucci.com/collections/loafers/products/ks524-12-button-up-loafer", "https://www.carrucci.com/collections/loafers/products/ks259-310-leather-loafer", "https://www.carrucci.com/collections/loafers/products/ks475-02p-carrucci-prom-loafer", 
#     "https://www.carrucci.com/collections/loafers/products/ks479-3002-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks625-101v-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks737-10a-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks737-02sb-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks2240-04sc-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks2024-01-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks1377-06p-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks502-11-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks308-01-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks261-04-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks261-03-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks261-02-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks259-11-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks142-03-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks099-9011-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks478-02-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks479-607-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks479-605-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks525-02p-carrucci-shoes", "https://www.carrucci.com/collections/loafers/products/ks525-102v-carrucci-velvet-loafer"
# ]
# make(loafers, "Loafer")

# oxfords = [
#     "https://www.carrucci.com/collections/oxford/products/ks886-25-carrucci-burnished-leather-blucher-1", "https://www.carrucci.com/collections/oxford/products/ks886-25-carrucci-burnished-leather-blucher", "https://www.carrucci.com/collections/oxford/products/ks509-25t-carrucci-two-tone-wingtip-oxford-2", "https://www.carrucci.com/collections/oxford/products/ks509-25t-carrucci-two-tone-wingtip-oxford-1", "https://www.carrucci.com/collections/oxford/products/ks509-25t-carrucci-two-tone-wingtip-oxford", "https://www.carrucci.com/collections/oxford/products/ks509-18-wingtip-slip-on-convertible-to-lace-up-4", "https://www.carrucci.com/collections/oxford/products/ks509-18-wingtip-slip-on-convertible-to-lace-up-3", "https://www.carrucci.com/collections/oxford/products/ks509-18-wingtip-slip-on-convertible-to-lace-up-2", "https://www.carrucci.com/collections/oxford/products/ks509-18-wingtip-slip-on-convertible-to-lace-up-1", "https://www.carrucci.com/collections/oxford/products/ks509-18-wingtip-slip-on-convertible-to-lace-up", "https://www.carrucci.com/collections/oxford/products/ks509-18-wingtip-slip-on-oxford", "https://www.carrucci.com/collections/oxford/products/ks509-25sc-carrucci-mixed-media-leather-oxford-6", "https://www.carrucci.com/collections/oxford/products/ks509-25sc-carrucci-mixed-media-leather-oxford-5", "https://www.carrucci.com/collections/oxford/products/ks509-25sc-carrucci-mixed-media-leather-oxford-4", "https://www.carrucci.com/collections/oxford/products/ks509-25sc-carrucci-mixed-media-leather-oxford-3", "https://www.carrucci.com/collections/oxford/products/ks509-25sc-carrucci-mixed-media-leather-oxford-2", "https://www.carrucci.com/collections/oxford/products/ks509-25sc-carrucci-mixed-media-leather-oxford-1", "https://www.carrucci.com/collections/oxford/products/ks509-25sc-carrucci-mixed-media-leather-oxford", "https://www.carrucci.com/collections/oxford/products/kb670-13-high-top-side-zipper-leather-sneaker-3", "https://www.carrucci.com/collections/oxford/products/kb670-13-high-top-side-zipper-leather-sneaker", "https://www.carrucci.com/collections/oxford/products/kb670-13-high-top-side-zipper-leather-sneaker-2", "https://www.carrucci.com/collections/oxford/products/kb670-13-high-top-side-zipper-leather-sneaker-1", "https://www.carrucci.com/collections/oxford/products/ks611-11-carrucci-burnished-leather-sneaker-3", "https://www.carrucci.com/collections/oxford/products/ks611-11-carrucci-burnished-leather-sneaker-2", 
#     "https://www.carrucci.com/collections/oxford/products/ks611-11-carrucci-burnished-leather-sneaker-1", "https://www.carrucci.com/collections/oxford/products/ks611-11-carrucci-burnished-leather-sneaker", "https://www.carrucci.com/collections/oxford/products/ks711-01-carrucci-wingtip-oxford", "https://www.carrucci.com/collections/oxford/products/ks886-14-hand-braided-leather-woven-oxford-2", "https://www.carrucci.com/collections/oxford/products/ks886-14-hand-braided-leather-woven-oxford-1", "https://www.carrucci.com/collections/oxford/products/ks886-14-hand-braided-leather-woven-oxford", "https://www.carrucci.com/collections/oxford/products/ks500-11-cap-toe-woven-leather-oxford-1", "https://www.carrucci.com/collections/oxford/products/ks500-11-cap-toe-woven-leather-oxford", "https://www.carrucci.com/collections/oxford/products/ks503-36-whole-cut-oxford", "https://www.carrucci.com/collections/oxford/products/ks711-02t-medallion-wingtip-leather-lace-up-2", "https://www.carrucci.com/collections/oxford/products/ks711-02t-medallion-wingtip-leather-lace-up-1", "https://www.carrucci.com/collections/oxford/products/ks711-01-medallion-cap-toe-leather-lace-up-2", "https://www.carrucci.com/collections/oxford/products/ks711-01-medallion-cap-toe-leather-lace-up-1", "https://www.carrucci.com/collections/oxford/products/ks711-01-medallion-cap-toe-leather-lace-up", "https://www.carrucci.com/collections/oxford/products/ks503-46-carrucci-hand-paint-lace-up-oxford", "https://www.carrucci.com/collections/oxford/products/ks503-46-carrucci-hand-paint-lace-up-oxford-1", "https://www.carrucci.com/collections/oxford/products/ks503-46-carrucci-hand-paint-lace-up-oxford-3", "https://www.carrucci.com/collections/oxford/products/ks503-46-carrucci-hand-paint-lace-up-oxford-2", "https://www.carrucci.com/collections/oxford/products/ks886-24-carrucci-removable-kiltie-buckle-loafer-2", "https://www.carrucci.com/collections/oxford/products/ks886-24-carrucci-removable-kiltie-buckle-loafer-1", "https://www.carrucci.com/collections/oxford/products/ks886-24-carrucci-removable-kiltie-buckle-loafer", "https://www.carrucci.com/collections/oxford/products/ks886-24-carrucci", "https://www.carrucci.com/collections/oxford/products/ks886-733-carrucci-perforated-cap-toe-oxford", "https://www.carrucci.com/collections/oxford/products/ks886-15-carrucci-wholecut-oxford", 
#     "https://www.carrucci.com/collections/oxford/products/ks479-04-carrucci-lace-up-oxford-1", "https://www.carrucci.com/collections/oxford/products/ks886-734-carrucci-wingtip-oxford-1", "https://www.carrucci.com/collections/oxford/products/ks886-734-carrucci-wingtip-oxford", "https://www.carrucci.com/collections/oxford/products/ks505-47-carrucci-wholecut-oxford-3", "https://www.carrucci.com/collections/oxford/products/ks505-47-carrucci-wholecut-oxford-2", "https://www.carrucci.com/collections/oxford/products/ks505-47-carrucci-wholecut-oxford-1", "https://www.carrucci.com/collections/oxford/products/ks505-47-carrucci-wholecut-oxford", "https://www.carrucci.com/collections/oxford/products/ks258-27s-carrucci-cap-toe-suede-lace-up-oxford", "https://www.carrucci.com/collections/oxford/products/ks524-203-carrucci-woven-split-toe-leather-oxford-2", "https://www.carrucci.com/collections/oxford/products/ks524-203-carrucci-woven-split-toe-leather-oxford-1", "https://www.carrucci.com/collections/oxford/products/ks524-203-carrucci-woven-split-toe-leather-oxford", "https://www.carrucci.com/collections/oxford/products/ks709-01-carrucci-graffiti-leather-oxford-2", "https://www.carrucci.com/collections/oxford/products/ks709-01-carrucci-graffiti-leather-oxford-1", "https://www.carrucci.com/collections/oxford/products/ks709-01-carrucci-graffiti-leather-oxford", "https://www.carrucci.com/collections/oxford/products/ks506-16-carrucci-slip-on-loafer-with-decorative-lace-up", "https://www.carrucci.com/collections/oxford/products/ks479-04-carrucci-lace-up-oxford", "https://www.carrucci.com/collections/oxford/products/ks099-721-cap-toe-leather-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks099-721-cap-toe-leather-oxford-brown-navy", "https://www.carrucci.com/collections/oxford/products/ks099-721-cap-toe-leather-oxford-brown", "https://www.carrucci.com/collections/oxford/products/ks099-603t-two-tone-leather-lace-up-brown-navy", "https://www.carrucci.com/collections/oxford/products/ks886-11t-hand-paint-wingtip-medallion-oxford-brown-cognac", "https://www.carrucci.com/collections/oxford/products/ks886-11t-hand-paint-wingtip-medallion-oxford-black-burgundy", "https://www.carrucci.com/collections/oxford/products/ks886-11t-hand-paint-wingtip-medallion-oxford-olive-brown", "https://www.carrucci.com/collections/oxford/products/ks886-11t-hand-paint-wingtip-medallion-oxford-brown-navy", 
#     "https://www.carrucci.com/collections/oxford/products/ks503-36-whole-cut-oxford-olive", "https://www.carrucci.com/collections/oxford/products/ks503-36-whole-cut-oxford-chestnut", "https://www.carrucci.com/collections/oxford/products/ks503-36-whole-cut-oxford-cognac", "https://www.carrucci.com/collections/oxford/products/ks308-03-lace-up-oxford-blue", "https://www.carrucci.com/collections/oxford/products/ks308-03-lace-up-oxford-brown", "https://www.carrucci.com/collections/oxford/products/ks308-03-lace-up-oxford-charcoal", "https://www.carrucci.com/collections/oxford/products/ks2240-01s-carrucci-leather-suede-slip-on-brown", "https://www.carrucci.com/collections/oxford/products/ks2240-01s-carrucci-leather-suede-slip-on-black", "https://www.carrucci.com/collections/oxford/products/ks2240-01s-carrucci-leather-suede-slip-on", "https://www.carrucci.com/collections/oxford/products/ks506-16-carrucci-slip-on-loafer-with-decorative-lace-up-navy", "https://www.carrucci.com/collections/oxford/products/ks506-16-carrucci-slip-on-loafer-with-decorative-lace-up-cognac", "https://www.carrucci.com/collections/oxford/products/ks735-01-soft-leather-lace-up-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks886-731-whole-cut-oxford-with-medallions-black", "https://www.carrucci.com/collections/oxford/products/ks886-731-whole-cut-oxford-with-medallions-burgundy", "https://www.carrucci.com/collections/oxford/products/ks886-731-whole-cut-oxford-with-medallions-navy", "https://www.carrucci.com/collections/oxford/products/ks886-731-whole-cut-oxford-with-medallions-cognac", "https://www.carrucci.com/collections/oxford/products/ks500-22-deerskin-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks500-22-deerskin-oxford-navy", "https://www.carrucci.com/collections/oxford/products/ks500-22-deerskin-oxford-burgundy", "https://www.carrucci.com/collections/oxford/products/ks500-22-deerskin-oxford-cognca", "https://www.carrucci.com/collections/oxford/products/ks099-813-wingtip-leather-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks099-813-wingtip-leather-oxford-brown", "https://www.carrucci.com/collections/oxford/products/ks099-721-cap-toe-leather-oxford-burgundy-black", "https://www.carrucci.com/collections/oxford/products/ks524-14-caviar-leather-oxford-grey", 
#     "https://www.carrucci.com/collections/oxford/products/ks524-14-caviar-leather-oxford-cognac", "https://www.carrucci.com/collections/oxford/products/ks524-14-caviar-leather-oxford-whisky", "https://www.carrucci.com/collections/oxford/products/ks479-04-lace-up-oxford-black-navy", "https://www.carrucci.com/collections/oxford/products/ks479-04-lace-up-oxford-cognac", "https://www.carrucci.com/collections/oxford/products/ks479-04-lace-up-oxford-chestnut", "https://www.carrucci.com/collections/oxford/products/ks479-04-lace-up-loafer-white", "https://www.carrucci.com/collections/oxford/products/ks524-14-caviar-leather-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks261-01-contrast-leather-oxford-blue-tan", "https://www.carrucci.com/collections/oxford/products/ks261-01-contrast-leather-oxford-navy", "https://www.carrucci.com/collections/oxford/products/ks261-01-contrast-leather-oxford-black-burg", "https://www.carrucci.com/collections/oxford/products/ks099-603t-two-tone-leather-lace-up-black-burgundy", "https://www.carrucci.com/collections/oxford/products/ks099-712-embossed-wingtip-oxford-oxblood", "https://www.carrucci.com/collections/oxford/products/ks099-712-embossed-wingtip-oxford-tan", "https://www.carrucci.com/collections/oxford/products/ks505-12-calfskin-lace-up-oxford-purple", "https://www.carrucci.com/collections/oxford/products/ks505-12-calfskin-lace-up-oxford-charcoal", "https://www.carrucci.com/collections/oxford/products/ks505-12-polished-calfskin-lace-up-oxford-olive", "https://www.carrucci.com/collections/oxford/products/ks505-12-calfskin-lace-up-oxford-cobalt", "https://www.carrucci.com/collections/oxford/products/ks505-12-polished-calfskin-lace-up-oxford-cognac", "https://www.carrucci.com/collections/oxford/products/ks505-12-calfskin-lace-up-oxford-burgndy", "https://www.carrucci.com/collections/oxford/products/ks505-11s-suede-lace-up-oxford-wheat", "https://www.carrucci.com/collections/oxford/products/ks505-11s-suede-lace-up-oxford-denim", "https://www.carrucci.com/collections/oxford/products/ks259-302-carrucci-timeless-lace-up-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks505-14s-suede-lace-up-oxford-burgundy", "https://www.carrucci.com/collections/oxford/products/ks505-14s-suede-lace-up-oxford-navy", 
#     "https://www.carrucci.com/collections/oxford/products/ks505-14s-suede-lace-up-oxford-dk-brown", "https://www.carrucci.com/collections/oxford/products/ks886-11cc-plaid-leather-wingtip-oxford-brown", "https://www.carrucci.com/collections/oxford/products/ks886-11cc-plaid-leather-wingtip-oxford", "https://www.carrucci.com/collections/oxford/products/ks524-12-button-up-loafer-black", "https://www.carrucci.com/collections/oxford/products/ks511-11m-matching-bottom-edge-oxford-gray", "https://www.carrucci.com/collections/oxford/products/ks511-11m-matching-bottom-edge-oxford-cognac", "https://www.carrucci.com/collections/oxford/products/ks511-11m-matching-bottom-edge-oxford-cobalt", "https://www.carrucci.com/collections/oxford/products/ks511-11-white-bottom-edge-oxford-burgundy", "https://www.carrucci.com/collections/oxford/products/ks511-11-white-bottom-edge-oxford-gray", "https://www.carrucci.com/collections/oxford/products/ks511-11-white-bottom-edge-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks511-11-white-bottom-edge-oxford-cognac", "https://www.carrucci.com/collections/oxford/products/ks511-11-white-bottom-edge-oxford-cobalt", "https://www.carrucci.com/collections/oxford/products/ks505-14s-suede-lace-up-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks505-12-calfskin-lace-up-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks505-11s-suede-lace-up-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks503-36a-color-lace-up-oxford-ocean-blue", "https://www.carrucci.com/collections/oxford/products/ks479-606-calfskin-oxford-cognac", "https://www.carrucci.com/collections/oxford/products/ks479-04-lace-up-loafer-burgundy", "https://www.carrucci.com/collections/oxford/products/ks479-04-lace-up-loafer-black", "https://www.carrucci.com/collections/oxford/products/ks478-16-burnished-leather-lace-up-black", "https://www.carrucci.com/collections/oxford/products/ks308-03-lace-up-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks259-12-woven-leather-lace-up-black", "https://www.carrucci.com/collections/oxford/products/ks2240-01-deerskin-oxford-black", "https://www.carrucci.com/collections/oxford/products/ks099-713-burnished-lace-up-oxford-navy",
#     "https://www.carrucci.com/collections/oxford/products/ks511-11m-matching-bottom-eva-outsle-oxford", "https://www.carrucci.com/collections/oxford/products/ks259-12", "https://www.carrucci.com/collections/oxford/products/ks478-16-carrucci-shoes", "https://www.carrucci.com/collections/oxford/products/ks099-601-carrucci-shoes", "https://www.carrucci.com/collections/oxford/products/ks261-01-carrucci-shoes", "https://www.carrucci.com/collections/oxford/products/ks259-13-carrucci-shoes", "https://www.carrucci.com/collections/oxford/products/ks142-04-carrucci-shoes", "https://www.carrucci.com/collections/oxford/products/ks142-02pc-carrucci-shoes", "https://www.carrucci.com/collections/oxford/products/ks099-713-carrucci-shoes", "https://www.carrucci.com/collections/oxford/products/ks099-712-carrucci-shoes", "https://www.carrucci.com/collections/oxford/products/ks503-36-carrucci-shoes", "https://www.carrucci.com/collections/oxford/products/ks511-11-carrucci-shoes", "https://www.carrucci.com/collections/oxford/products/ks525-01p-carrucci-shoes"
# ]
# make(oxfords, "Oxford")

# boots = [
#     "https://www.carrucci.com/collections/boots/products/ks509-11-carrucci-chukka-boots", "https://www.carrucci.com/collections/boots/products/kb670-13-high-top-side-zipper-leather-sneaker-3", "https://www.carrucci.com/collections/boots/products/kb670-13-high-top-side-zipper-leather-sneaker", "https://www.carrucci.com/collections/boots/products/kb670-13-high-top-side-zipper-leather-sneaker-2", "https://www.carrucci.com/collections/boots/products/kb670-13-high-top-side-zipper-leather-sneaker-1", "https://www.carrucci.com/collections/boots/products/kb886-17-strap-buckle-leather-boots", "https://www.carrucci.com/collections/boots/products/kb886-17-buckle-leather-strap-boots", "https://www.carrucci.com/collections/boots/products/kb886-17-leather-strap-buckle-boots-1", "https://www.carrucci.com/collections/boots/products/kb478-108s-leather-suede-chelsea-high-boots-4", "https://www.carrucci.com/collections/boots/products/kb478-108s-leather-suede-chelsea-high-boots-3", "https://www.carrucci.com/collections/boots/products/kb478-108s-leather-suede-chelsea-high-boots", "https://www.carrucci.com/collections/boots/products/kb478-108s-leather-suede-chelsea-high-boots-2", "https://www.carrucci.com/collections/boots/products/kb478-108s-leather-suede-chelsea-high-boots-1", "https://www.carrucci.com/collections/boots/products/kb478-107s-leather-suede-chelsea-boots-2", "https://www.carrucci.com/collections/boots/products/kb478-107s-leather-suede-chelsea-boots-1", "https://www.carrucci.com/collections/boots/products/kb478-107s-leather-suede-chelsea-boots", "https://www.carrucci.com/collections/boots/products/kb503-13-calfskin-lace-up-chukka-boots-2", "https://www.carrucci.com/collections/boots/products/kb503-13-calfskin-lace-up-chukka-boots-1", "https://www.carrucci.com/collections/boots/products/kb503-13-calfskin-lace-up-chukka-boots", "https://www.carrucci.com/collections/boots/products/kb503-13-calf-skin-lace-up-chukka-boots-1", "https://www.carrucci.com/collections/boots/products/kb503-13-calf-skin-lace-up-chukka-boots", "https://www.carrucci.com/collections/boots/products/kb1377-05-carrucci-chelsea-boots-1", "https://www.carrucci.com/collections/boots/products/kb1377-05-carrucci-chelsea-boots-black", "https://www.carrucci.com/collections/boots/products/kb1377-05-carrucci-chelsea-boots", 
#     "https://www.carrucci.com/collections/boots/products/kb524-13-lace-up-zip-boots-navy-olive-cognac", "https://www.carrucci.com/collections/boots/products/kb524-13-lace-up-zip-boots-tri-color-brown", "https://www.carrucci.com/collections/boots/products/kb503-01s-leather-suede-chelsea-boots-burgundy", "https://www.carrucci.com/collections/boots/products/kb503-01s-leather-suede-chelsea-boots-saddle", "https://www.carrucci.com/collections/boots/products/kb503-01s-leather-suede-chelsea-boots-sand", "https://www.carrucci.com/collections/boots/products/kb503-01s-leather-suede-chelsea-boots-black", "https://www.carrucci.com/collections/boots/products/kb503-01s-leather-suede-chelsea-boots-dk-brown", "https://www.carrucci.com/collections/boots/products/kb478-11-hand-burnished-chelsea-boots-black-red", "https://www.carrucci.com/collections/boots/products/kb478-11-hand-burnished-chelsea-boots-grey", "https://www.carrucci.com/collections/boots/products/kb478-11-hand-burnished-chelsea-boots-red", "https://www.carrucci.com/collections/boots/products/kb478-11-hand-burnished-chelsea-boots-olive", "https://www.carrucci.com/collections/boots/products/kb478-11-hand-burnished-chelsea-boots-purple", "https://www.carrucci.com/collections/boots/products/kb478-11-hand-burnished-chelsea-boots-navy", "https://www.carrucci.com/collections/boots/products/kb478-11-hand-burnished-chelsea-boots-cognac", "https://www.carrucci.com/collections/boots/products/kb735-11n-carrucci-red-stitches-leather-boots", "https://www.carrucci.com/collections/boots/products/kb8018-15-carrucci-buckle-boots", "https://www.carrucci.com/collections/boots/products/kb2019-11-carrucci-chelsea-boots", "https://www.carrucci.com/collections/boots/products/kb524-12-carrucci-button-up-denim-zip-boots", "https://www.carrucci.com/collections/boots/products/kb470-01-burnished-zip-boots-brown", "https://www.carrucci.com/collections/boots/products/kb8018-16-monk-strap-zip-boots-cognac", "https://www.carrucci.com/collections/boots/products/kb524-11sc-carrucci-lace-up-suede-boots-cognac", "https://www.carrucci.com/collections/boots/products/kb524-11sc-carrucci-lace-up-suede-boots-burgundy", "https://www.carrucci.com/collections/boots/products/kb524-13-lace-up-zip-boots-charcoal", "https://www.carrucci.com/collections/boots/products/kb8018-16-monk-strap-buckle-boots-black", 
#     "https://www.carrucci.com/collections/boots/products/kb478-11-burnished-leather-boots-black", "https://www.carrucci.com/collections/boots/products/kb470-01-burnished-leather-boots-black", "https://www.carrucci.com/collections/boots/products/kb2019-13-burnished-leather-boots-black", "https://www.carrucci.com/collections/boots/products/kb43-05-carrucci-boots", "https://www.carrucci.com/collections/boots/products/kb2019-13-carrucci-boots", "https://www.carrucci.com/collections/boots/products/kb1377-05e-carrucci-boots", "https://www.carrucci.com/collections/boots/products/kb524-11sc-carrucci-boots", "https://www.carrucci.com/collections/boots/products/kb524-12cc-carrucci-boots", "https://www.carrucci.com/collections/boots/products/kb524-12dc-carrucci-boots", "https://www.carrucci.com/collections/boots/products/kb524-12sc-carrucci-boots"
# ]
# make(boots, "Boot")

# distinct = []
# for p in products:
#     if p.handle not in distinct:
#         distinct.append(p)

# print(len(products))
# print(len(distinct))
# productstocsv(distinct)
# productstoinventory(distinct)
# productstoinventory(csvtoproducts('products_export_1.csv'))

