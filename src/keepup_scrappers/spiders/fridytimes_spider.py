import scrapy
import json
import logging
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import FridayTItem

class FridayTimesSpider(BaseSpider):
    
    name = 'ft_spider'
    page_counter = 0
    
    custom_settings = {
        "USER_AGENT" : 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
        "IMAGES_STORE": 'data/fridaytimes/images/',
        "FEEDS": {
            "data/fridaytimes/data.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
            },
        }
    }

    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = 'fridaytimesfactcheck'
        super().__init__(*args, **kwargs)

    def get_payload_headers(self, page_no):
        
        payload = {
            'post_per_page': '20',
            'post_listing_limit_offset': str(page_no),
            'directory_name': 'categories_pages',
            'template_name': 'lazy_loading',
            'category_name': 'fact-check',
        }

        return payload
    
    def start_requests(self):     
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse)

    def parse(self, response):
        if response.text.strip() == "no_more_news":
            self.logger.warning("No more news available. Stopping.")
            return
        
        for post in response.css(self.selectors['single_post']):

            item = FridayTItem()

            item['title'] = post.css(self.selectors['post_title']).get().strip()
            image_url = post.css(self.selectors['post_image']).get()
            item['image_urls'] = [response.urljoin(image_url)]   
            item['detail_url'] = post.css(self.selectors['post_link']).get()

            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_details,
                meta={'item': item},
            )
        
        self.page_counter += 20
        self.logger.info(f"Completed offset {self.page_counter - 20}")
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse)


    def parse_details(self, response):
        item = response.meta['item']
        item['publication_date'] = response.css(self.selectors['post_date']).get()
        item['content'] = ' '.join(response.css(self.selectors['content']).getall())

        yield item
