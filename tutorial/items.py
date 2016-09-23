import scrapy

class ProductItem(scrapy.Item):
    seccode = scrapy.Field()
    unitnv = scrapy.Field()
    accumulatedUnitnv = scrapy.Field()
    manageFee = scrapy.Field()
    trustFee = scrapy.Field()
    flag = scrapy.Field()
    comeFrom = scrapy.Field()
    updateDate = scrapy.Field() 
