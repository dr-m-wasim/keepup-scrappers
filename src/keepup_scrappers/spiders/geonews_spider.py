import scrapy
import json
import logging
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import GeoNewsItem

class GNSpider(BaseSpider):
    
    name = 'gn_spider'
    page_counter = 1
    
    custom_settings = {
        "USER_AGENT" : 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
        "IMAGES_STORE": 'data/geonews/images/',
        "FEEDS": {
            "data/geonews/data.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
            },
        }
    }

    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = 'geonews'
        super().__init__(*args, **kwargs)

    

    def parse(self, response):
       
        for post in response.css(self.selectors['single_post']):

            item = GeoNewsItem()

            item['title'] = post.css(self.selectors['post_title']).get()
            
               
            item['detail_url'] = post.css(self.selectors['post_link']).get()
            

            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_details,
                meta={'item': item},
            )


        

    def parse_details(self, response):
        item = response.meta['item']
        item['author'] = response.css(self.selectors['author']).get()
        item['content'] = ' '.join(response.css(self.selectors['content']).getall()).strip()
        item['publication_date'] = response.css(self.selectors['post_date']).get().strip()
        image_url = response.css(self.selectors['post_image']).get()
        item['image_urls'] = [response.urljoin(image_url)]

        yield item