import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import BBCItem
import json
import logging

class BBCSpider(BaseSpider):
    
    name = 'bbc_spider'
    site_key = 'bbc'
    page_counter = 1
    custom_settings = {
            "IMAGES_STORE": f'data/{site_key}/images/',
            "FEEDS": {
                f"data/{site_key}/data.json": {
                    "format": "json",
                    "encoding": "utf8",
                    "indent": 4,
                }
            },
        'ROBOTSTXT_OBEY': False
        }
    
    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = self.site_key
        super().__init__(*args, **kwargs)

    def get_payload_headers(self, page_no):
        
        payload = {
            'action': 'load_latest_posts',
            'page': str(page_no)
        }

        return payload
    
    def start_requests(self):     
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.Request(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse)

    def parse(self, response):
        self.log(f"Processing Page {self.page_counter}", level = logging.INFO)
        #data = json.loads(response.text)
        json_response = response.json()
        # Check if there's more data to scrape
        has_more = json_response.get('data', {}).get('has_more', False)

        for post in json_response.get('data', []):
            item = BBCItem()

            item['title'] = post.get('title', '')
            relative_url = post.get('path', '')
            item['detail_url'] = response.urljoin(relative_url)
            item['country'] = post.get('topics', [])
            item['exerpt'] = [post.get('summary', '')]

            relative_url = post.get('path', '')
            item['detail_url'] = response.urljoin(relative_url)

            
            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_details,
                meta={'item': item},
                errback=self.handle_error,
            )
        if has_more:
            self.page_counter += 1
            payload = self.get_payload_headers(self.page_counter)

            # Request the next page of data
            yield scrapy.Request(
                url=self.start_urls[0], 
                formdata=payload, 
                callback=self.parse,
                errback=self.handle_error,
            )
        self.logger.info(f"Page {self.page_counter} completed")

    def parse_details(self, response):
        item = response.meta['item']
        item['publication_date'] = response.css(self.selectors['post_date']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    
    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")



