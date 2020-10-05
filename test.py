from product import *
from inventory import *

original = csvtoproducts('products - Copy.csv')
current = csvtoproducts('current.csv')

otitles = [p.title for p in original]
ctitles = [p.title for p in current]

for c in current:
    if c.title in otitles:
        for o in original:
            if c.title == o.title:
                c.price = o.price

i = 0
for o in original:
    if o.title not in ctitles:
        current.append(o)
        # print(i)
        # i += 1

for c in current:
    c.inventory = []
    for i in range(11):
        c.inventory.append((1, 0))
# productstocsv(current)
productstoinventory(current)