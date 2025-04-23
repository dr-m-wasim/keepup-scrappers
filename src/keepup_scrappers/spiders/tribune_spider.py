import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import TribuneItem
import time

class tribuneSpider(BaseSpider):
    
    name = 'tribune_spider'
    site_key = 'tribune'

    
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

            item = TribuneItem()

            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='').strip()

            if item['detail_url']:
                yield scrapy.Request(
                    url=item['detail_url'],
                    callback=self.parse_details,
                    meta={'item': item},
                    errback=self.handle_error,
                )
        
        self.logger.info(f"Page {self.page_counter} completed")
        self.page_counter += 1

        is_next_page_disabled = len(response.css('ul.pagination li.disabled').getall()) 
        
        if self.page_counter == 2 or not is_next_page_disabled:
            yield scrapy.Request(
                url=response.urljoin(f'/latest?page={self.page_counter}'),
                callback=self.parse,
                errback=self.handle_error,
            )

    def parse_details(self, response):
        item = response.meta['item']
        #image_url = response.css(self.selectors['post_image']).get(default='')
        #item['image_urls'] = [response.urljoin(image_url)] if image_url else []
        item['catagory'] = response.css(self.selectors['catagory']).get(default='')
        item['content'] = ' '.join(response.css(self.selectors['content']).getall()).strip()
        item['publication_date'] = response.css(self.selectors['post_date']).getall()
        cleaned_dates = [text.strip() for text in item['publication_date'] if text.strip()]
        if cleaned_dates:
            item['publication_date'] = cleaned_dates[0]
        else:
            item['publication_date'] = None
        

        yield item
    
    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")