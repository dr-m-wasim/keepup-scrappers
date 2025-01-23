import scrapy
import json
import logging
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import PolitifactItem

class PolitifactSpider(BaseSpider):
    
    name = 'politifact_spider'
    page_counter = 1
    
    custom_settings = {
        "USER_AGENT" : 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
        "IMAGES_STORE": 'data/politifact/images/',
        "FEEDS": {
            "data/politifact/data.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
            },
        }
    }

    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = 'politifact'
        super().__init__(*args, **kwargs)
        self.page_counter = 1

    def parse(self, response):
        for post in response.css(self.selectors['single_post']):

            item = PolitifactItem()

            item['title'] = post.css(self.selectors['post_title']).get().strip()
            relative_url = post.css(self.selectors['post_link']).get()
            item['detail_url'] = response.urljoin(relative_url)
            item['label'] = response.css(self.selectors['label']).get().strip()

            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_details,
                meta={'item': item},
            )

        self.logger.info(f"Page {self.page_counter} completed")
        self.page_counter += 1
        next_page = response.xpath(self.selectors['next_page']).get() 
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse,
            )

        
    def parse_details(self, response):
        item = response.meta['item']
        item['author'] = response.css(self.selectors['author']).get()
        item['content'] = ' '.join(response.css(self.selectors['content']).getall()).strip()
        item['publication_date'] = response.css(self.selectors['post_date']).get().strip()
        image_url = response.css(self.selectors['post_image']).get()
        item['image_urls'] = [response.urljoin(image_url)]

        yield item