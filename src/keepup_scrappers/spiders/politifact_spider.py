import scrapy
import json
import logging
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import PolitifactItem

class PolitifactSpider(BaseSpider):
    
    name = 'politifact_spider'
    page_counter = 1
    site_key = 'politifact'
    
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

            item = PolitifactItem()

            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            relative_url = post.css(self.selectors['post_link']).get(default='')
            item['detail_url'] = response.urljoin(relative_url) if relative_url else [] 
            item['label'] = response.css(self.selectors['label']).get(default='').strip()

            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_details,
                meta={'item': item},
                errback=self.handle_error,
            )

        self.logger.info(f"Page {self.page_counter} completed")
        self.page_counter += 1
        next_page = response.xpath(self.selectors['next_page']).get() 
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse,
                errback=self.handle_error,
            )

        
    def parse_details(self, response):
        item = response.meta['item']
        item['author'] = response.css(self.selectors['author']).get(default='').strip()
        item['publication_date'] = response.css(self.selectors['post_date']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])
        image_url = response.css(self.selectors['post_image']).get(default='')
        item['image_urls'] = [response.urljoin(image_url)] if image_url else [] 

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")