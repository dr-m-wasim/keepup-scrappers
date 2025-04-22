import scrapy
import json
import logging
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import SnopesItem

class SnopesSpider(BaseSpider):
    
    name = 'snopes_spider'
    page_counter = 1
    site_key = 'snopes'
    
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
        self.page_counter = 1

    def parse(self, response):
        for post in response.css(self.selectors['single_post']):

            item = SnopesItem()

            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            #image_url = post.css(self.selectors['post_image']).get(default='')
            #item['image_urls'] = [response.urljoin(image_url)] if image_url else []   
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='')
            item['publication_date'] = post.css(self.selectors['post_date']).get(default='').strip()
            item['author'] = post.css(self.selectors['author']).get(default='')

            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_details,
                meta={'item': item},
                errback=self.handle_error,
            )

        self.logger.info(f"Page {self.page_counter} completed")
        self.page_counter += 1

        next_btn = response.css(self.selectors['next_btn']).get() 

        next_page = response.css(self.selectors['next_page']).get() 
        
        if not 'disabled' in next_btn:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse,
                errback=self.handle_error,
            )
        
    def parse_details(self, response):
        item = response.meta['item']
        item['label'] = response.css(self.selectors['label']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")