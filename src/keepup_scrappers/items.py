import scrapy

class SochFactcheckItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field() 
    label = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    categories = scrapy.Field()
    publication_date = scrapy.Field()

class PakIVerifyItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    label = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class GeofactcheckItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class ThefridaytimesfactcheckItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()

class GeoNewsItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field() 
    content = scrapy.Field()
    author = scrapy.Field()
    publication_date = scrapy.Field()
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
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    label = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
class TribuneItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    catagory = scrapy.Field()
class ReutersItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    label = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    claim = scrapy.Field()

class DawnnewsItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class DWfactcheckItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    #images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    exerpt = scrapy.Field()
    category = scrapy.Field()
    label = scrapy.Field()

class HumEnglishFactcheckItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    exerpt = scrapy.Field()
    label = scrapy.Field()
class FactcheckorgItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
class BRecorderItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    category = scrapy.Field()
    exerpt = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class DailytimesItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    exerpt = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()


class AljazeeraItem(scrapy.Item):
    title = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    exerpt = scrapy.Field()

class DunyaNewsItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()

class HumEnglishItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    detail_url = scrapy.Field()
    exerpt = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class JangItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    exerpt = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    #category = scrapy.Field()


class TheNationItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class ThehinduItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    exerpt = scrapy.Field()
    publication_date = scrapy.Field()
    author = scrapy.Field()

class PakistanTodayItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    exerpt = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class SamaaTVItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    exerpt = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class AryNewsItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    detail_url = scrapy.Field()
    exerpt = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()

class BBCItem(scrapy.Item):
    title = scrapy.Field()
    exerpt = scrapy.Field()
    country = scrapy.Field()
    detail_url = scrapy.Field() 
    content = scrapy.Field()
    publication_date = scrapy.Field()

class TheNewsItem(scrapy.Item):
    title = scrapy.Field()
    detail_url = scrapy.Field()
    exerpt = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    author = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()

class BolNewsItem(scrapy.Item):
    title = scrapy.Field()
    detail_url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    author = scrapy.Field()
    publication_date = scrapy.Field()
    content = scrapy.Field()