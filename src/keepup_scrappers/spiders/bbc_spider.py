import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import BBCItem
import json
import logging
from urllib.parse import urljoin

class BBCSpider(BaseSpider):
    
    name = 'bbc_spider'
    site_key = 'bbc'
    page_counter = 0
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
        
    
    def start_requests(self):   
        
        url = f'{self.start_urls[0]}?page={self.page_counter}'
        self.logger.info(f"Requesting page {self.page_counter}: {url}")
        yield scrapy.FormRequest(url = self.start_urls[0], 
                                    #formdata = payload, 
                                    callback = self.parse)

    def parse(self, response):
        

        json_response = response.json()

         # Check if there are posts to scrape
        posts = json_response.get('data', [])
        if not posts:
            self.logger.info(f"No posts found on page {self.page_counter}. Stopping scraping.")
            return  # Stop scraping when there are no posts

        id = json_response.get('page', '')
        
        
        for post in json_response.get('data', []):
            item = BBCItem()
        
            item['title'] = post.get('title', '')
            relative_url = post.get('path', '')
            item['detail_url'] = urljoin("https://www.bbc.com/", relative_url)
            item['country'] = post.get('topics', [])
            item['exerpt'] = [post.get('summary', '')]
            
            yield scrapy.Request(
                url = item['detail_url'],
                callback = self.parse_details,
                meta = {'item': item},
                errback=self.handle_error,
            )

        self.page_counter += 1

        # Request the next page
        next_page_url = f'{self.start_urls[0]}page={self.page_counter}'
        self.logger.info(f"Requesting next page: {next_page_url}")
        
        yield scrapy.FormRequest(url=next_page_url, callback=self.parse)
        
    def parse_details(self, response):
        item = response.meta['item']
        item['publication_date'] = response.css(self.selectors['post_date']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    
    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")



