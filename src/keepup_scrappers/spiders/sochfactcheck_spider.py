import scrapy
import json
import logging
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import SochFactcheckItem

class SochFactCheckSpider(BaseSpider):
    
    name = 'sochfactcheck_spider'
    page_counter = 1
    site_key = 'sochfactcheck'
    
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
            'action': 'load_latest_posts',
            'page': str(page_no)
        }

        return payload
    
    def start_requests(self):     
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse)

    def parse(self, response):
        
        self.log(f"Processing Page {self.page_counter}", level = logging.INFO)

        # Parse the JSON response
        data = json.loads(response.text)
        all_posts = scrapy.Selector(text=data['data']['posts'], type="html")
        
        for post in all_posts.css(self.selectors['single_post']).getall():
            parsed_post = scrapy.Selector(text=post, type="html")
            
            item = SochFactcheckItem()

            item['title'] = parsed_post.css(self.selectors['post_title']).get(default='').strip()
            image_url = parsed_post.css(self.selectors['post_image']).get(default='')
            item['image_urls'] = [response.urljoin(image_url)] if image_url else []     # urljoin is required to accomodate relative paths
            item['detail_url'] = parsed_post.css(self.selectors['post_link']).get(default='').strip()
            item['label'] = parsed_post.css(self.selectors['label']).get(default='').strip()
            item['categories'] = parsed_post.css(self.selectors['post_cat']).getall()
            item['publication_date'] = parsed_post.css(self.selectors['post_date']).get(default='').strip()

            # Follow the link to the detail page
            yield response.follow(item['detail_url'], 
                                  self.parse_details, 
                                  meta={'item': item},
                                  errback=self.handle_error,)

        has_more = data['data']['has_more']
        
        if has_more:
            self.page_counter += 1
            payload = self.get_payload_headers(self.page_counter)

            yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse,
                                 errback=self.handle_error,)
            
    def parse_details(self, response):
        # Extract additional details from the detail page
        item = response.meta['item']
        
        item['author'] = response.css(self.selectors['author']).get(default='')
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])
        
        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")