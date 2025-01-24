import scrapy
import json
import logging
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import FridayTItem

class FridayTimesSpider(BaseSpider):
    
    name = 'ft_spider'
    site_key = 'fridaytimesfactcheck'
    page_counter = 0
    
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

            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            image_url = post.css(self.selectors['post_image']).get(default='')
            item['image_urls'] = [response.urljoin(image_url)] if image_url else []  
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='')

            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_details,
                meta={'item': item},
                errback=self.handle_error,
            )
        
        self.page_counter += 20
        self.logger.info(f"Completed offset {self.page_counter - 20}")
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse,
                                 errback=self.handle_error,)


    def parse_details(self, response):
        item = response.meta['item']
        item['publication_date'] = response.css(self.selectors['post_date']).get(default='')

        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")
