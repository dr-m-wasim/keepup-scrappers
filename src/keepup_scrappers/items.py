import scrapy

class SFCItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field() 
    content = scrapy.Field()
    author = scrapy.Field()
    categories = scrapy.Field()
    publication_date = scrapy.Field()

class IVerifyItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    label = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class GFCItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class FridayTItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()

class SnopesItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    label = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class PolitifactItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    label = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()