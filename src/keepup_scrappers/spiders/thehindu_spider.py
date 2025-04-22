import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import ThehinduItem
import scrapy
import time

class ThehinduSpider(BaseSpider):
    
    name = 'thehindu_spider'
    page_counter = 1
    site_key = 'thehindu'
    
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

    def start_requests(self):     
        yield scrapy.Request(
            url= self.start_urls[0],
            meta={"playwright": True},
            callback = self.parse,
        )

    def parse(self, response):
        time.sleep(5)
        for post in response.css(self.selectors['single_post']):
            item = ThehinduItem()
            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            #image_url = post.css(self.selectors['post_image']).get(default='')
            #item['image_urls'] = [response.urljoin(image_url)] if image_url else []   
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='')
            
            item['author'] = post.css(self.selectors['author']).get(default='')

            if item['detail_url']:
                yield scrapy.Request(
                    url=item['detail_url'],
                    callback=self.parse_details,
                    meta={'item': item},
                    errback=self.handle_error,
                )

        # self.logger.info(f"Page {self.page_counter} completed")
        # self.page_counter += 1
        # get_next_page = response.css(self.selectors['next_page']).get()
        # next_page = response.urljoin(get_next_page) 
        # if next_page:
        #     yield scrapy.Request(
        #         url=response.urljoin(next_page),
        #         callback=self.parse,
        #         errback=self.handle_error,
        #     )
        self.logger.info(f"Page {self.page_counter} completed")
        self.page_counter += 1

        get_next_page = response.css(self.selectors['next_page']).get()
        if get_next_page:
            next_page = response.urljoin(get_next_page)
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                errback=self.handle_error,
            )

    def parse_details(self, response):
        item = response.meta['item']
        item['exerpt'] = response.css(self.selectors['exerpt']).get(default='')
        item['publication_date'] = response.css(self.selectors['post_date']).get(default='').strip()

        yield item
    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")

    