import scrapy
import json
import logging
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import GFCItem

class GFCSpider(BaseSpider):
    
    name = 'gfc_spider'
    page_counter = 1
    
    custom_settings = {
        "USER_AGENT" : 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
        "IMAGES_STORE": 'data/geofactcheck/images/',
        "FEEDS": {
            "data/geofactcheck/data.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
            },
        }
    }

    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = 'geofactcheck'
        super().__init__(*args, **kwargs)

    def get_payload_headers(self, page_no):
        
        payload = {
            'offset': str(page_no),
            'tag': '0'
        }

        return payload
    
    def start_requests(self):     
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse)

    def parse(self, response):
        if not response.body.strip():
            self.logger.warning("Empty response received.")
            return
        for post in response.css(self.selectors['single_post']):

            item = GFCItem()

            item['title'] = post.css(self.selectors['post_title']).get()
            image_url = post.css(self.selectors['post_image']).get()
            item['image_urls'] = [response.urljoin(image_url)]   
            item['detail_url'] = post.css(self.selectors['post_link']).get()
            item['publication_date'] = post.css(self.selectors['post_date']).get()

            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_details,
                meta={'item': item},
            )


        self.page_counter += 1
        self.logger.info(f"Completed page {self.page_counter - 1}")
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse)
        

    def parse_details(self, response):
        item = response.meta['item']
        item['author'] = response.xpath(self.selectors['author']).get()
        item['content'] = ' '.join(response.css(self.selectors['content']).getall()).strip()

        yield item