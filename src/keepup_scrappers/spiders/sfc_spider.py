import scrapy
import json
import logging
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import SFCItem

class SFCSpider(BaseSpider):
    
    name = 'sochfactcheck_spider'
    page_counter = 1
    
    custom_settings = {
        "ITEM_PIPELINES": {'keepup_scrappers.pipelines.CustomImagesPipeline': 1},
        "IMAGES_STORE": '../data/images/',
        "FEEDS": {
            "../data/sochfactcheck/data.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
            },
        }
    }

    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = 'sochfactcheck'
        super().__init__(*args, **kwargs)

    def get_payload_headers(self, page_no):
        
        payload = {
            'action': 'load_latest_posts',
            'page': str(page_no)
        }
        
        headers = {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }

        return payload, headers
    
    def start_requests(self):     
        payload, headers = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 headers = headers, 
                                 callback = self.parse)

    def parse(self, response):
        
        self.log(f"Processing Page {self.page_counter}", level = logging.INFO)

        # Parse the JSON response
        data = json.loads(response.text)
        all_posts = scrapy.Selector(text=data['data']['posts'], type="html")
        
        for post in all_posts.css(self.selectors['single_post']).getall():
            parsed_post = scrapy.Selector(text=post, type="html")
            
            item = SFCItem()

            item['title'] = parsed_post.css(self.selectors['post_title']).get().strip()
            image_url = parsed_post.css(self.selectors['post_image']).get()
            item['image_urls'] = [response.urljoin(image_url)]    # urljoin is required to accomodate relative paths
            item['detail_url'] = parsed_post.css(self.selectors['post_link']).get().strip()
            item['categories'] = parsed_post.css(self.selectors['post_cat']).getall()
            item['publication_date'] = parsed_post.css(self.selectors['post_date']).get().strip()

            # Follow the link to the detail page
            yield response.follow(item['detail_url'], self.parse_details, meta={'item': item})

        has_more = data['data']['has_more']
        
        if has_more:
            self.page_counter += 1
            payload, headers = self.get_payload_headers(self.page_counter)

            yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 headers = headers, 
                                 callback = self.parse)
            
    def parse_details(self, response):
        # Extract additional details from the detail page
        item = response.meta['item']
        
        item['author'] = response.css(self.selectors['author']).get()
        item['content'] = response.css(self.selectors['content']).get()
        
        yield item