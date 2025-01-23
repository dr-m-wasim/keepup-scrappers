import scrapy
import json
import logging
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import TribuneItem

class tribuneSpider(BaseSpider):
    
    name = 'tribune_spider'
    
    custom_settings = {
        "USER_AGENT" : 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
        "IMAGES_STORE": 'data/tribune/images/',
        "FEEDS": {
            "data/tribune/data.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
            },
        }
    }

    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = 'tribune'
        super().__init__(*args, **kwargs)
        self.page_counter = 1


    def parse(self, response):
        
        for post in response.css(self.selectors['single_post']):

            item = TribuneItem()

            #print('---', post.css(self.selectors['post_title']))

            item['title'] = post.css(self.selectors['post_title']).get().strip()
            image_url = post.css(self.selectors['post_image']).get()
            item['image_urls'] = [response.urljoin(image_url)]
            item['detail_url'] = post.css(self.selectors['post_link']).get().strip()
            

            
            

            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_details,
                meta={'item': item},
            )
        
        print(f"Page {self.page_counter} completed")
        self.page_counter += 1

        next_page = response.css(self.selectors['next_page']).get() 
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse,
            )

    def parse_details(self, response):
        item = response.meta['item']
        item['catagory'] = response.css(self.selectors['catagory']).get()
        item['content'] = ' '.join(response.css(self.selectors['content']).getall()).strip()
        item['publication_date'] = response.css(self.selectors['post_date']).getall()
        cleaned_dates = [text.strip() for text in item['publication_date'] if text.strip()]
        if cleaned_dates:
            item['publication_date'] = cleaned_dates[0]
        else:
            item['publication_date'] = None
        

        yield item
