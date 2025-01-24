import scrapy
import json
import logging
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import GeoNewsItem

class GNSpider(BaseSpider):
    
    name = 'gn_spider'

    site_key = 'geonews'
    #page_counter = 1
    
    custom_settings = {
        "IMAGES_STORE": f'data/{site_key}/images/',
            "FEEDS": {
                f"data/{site_key}/data.json": {
                    "format": "json",
                    "encoding": "utf8",
                    "indent": 4,
                }
            }
        }

    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = self.site_key
        super().__init__(*args, **kwargs)

    
    def parse(self, response):
       
        for post in response.css(self.selectors['single_post']):
            
            item = GeoNewsItem()

            item['title'] = post.css(self.selectors['post_title']).get(default='').strip() 
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='').strip()
            

            if item['detail_url']:
                yield scrapy.Request(
                    url=item['detail_url'],
                    callback=self.parse_details,
                    meta={'item': item},
                    errback=self.handle_error,
                )


    def parse_details(self, response):
        item = response.meta['item']
        item['author'] = response.css(self.selectors['author']).get()
        item['content'] = ' '.join(response.css(self.selectors['content']).getall()).strip()
        item['publication_date'] = response.css(self.selectors['post_date']).get(default='').strip()
        image_url = response.css(self.selectors['post_image']).get(default='')
        item['image_urls'] = [response.urljoin(image_url)] if image_url else []

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")