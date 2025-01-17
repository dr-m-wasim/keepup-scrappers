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