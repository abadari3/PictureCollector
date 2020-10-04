class product:
    def __init__(self, handle = None, title = None, body = None, vendor = None, type = None, tags = None, sizes = None, colors = None, price = None, oldprice = None, barcode = None, images = None, seotitle = None, seodescription = None, sku = None, published = "TRUE", taxable = "TRUE", inventory = None):
        if handle is None:
            handle = ""
        if title is None:
            title = ""
        if body is None:
            body = ""
        if vendor is None:
            vendor = ""
        if type is None:
            type = ""
        if tags is None:
            tags = []
        if sizes is None:
            sizes = []
        if colors is None:
            colors = []
        if price is None:
            price = []
        if oldprice is None:
            oldprice = []
        if barcode is None:
            barcode = []
        if images is None:
            images = []
        if seotitle is None:
            seotitle = ""
        if seodescription is None:
            seodescription = ""
        if sku is None:
            sku = []
        if inventory is None:
            inventory = []
        self.handle = handle
        self.title = title
        self.body = body
        self.vendor = vendor
        self.type = type
        self.tags = tags
        self.sizes = sizes
        self.colors = colors
        self.price = price
        self.oldprice = oldprice
        self.barcode = barcode
        self.images = images
        self.seotitle = seotitle
        self.seodescription = seodescription
        self.sku = sku
        self.published = published
        self.taxable = taxable
        self.inventory = inventory
    
    def __str__(self):
        string = ""
        string += self.title + "\n----------------------------------"+"\nHandle: \t" + self.handle
        string += "\nSizes: \t\t" + str(self.sizes)
        string += "\nColors: \t" + str(self.colors)
        string += "\nSKU: \t\t" + str(self.sku)
        string += "\nImages: \t" + str(self.images)
        string += "\n-----------------------------------\n"
        return string