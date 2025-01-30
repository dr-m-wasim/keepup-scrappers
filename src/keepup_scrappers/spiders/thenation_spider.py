import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import TheNationItem
import re

class TheNationSpider(BaseSpider):
    
    name = 'thenation_spider'
    site_key = 'thenation'
    page_counter = 36
    
    custom_settings = {
            "IMAGES_STORE": f'data/{site_key}/images/',
            "FEEDS": {
                f"data/{site_key}/data.json": {
                    "format": "json",
                    "encoding": "utf8",
                    "indent": 4,
                }
            },
            'ROBOTSTXT_OBEY': False,
            'DOWNLOAD_DELAY': 2
        }
    
    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = self.site_key
        super().__init__(*args, **kwargs)

    def get_payload_headers(self, page_no):
        
        payload = {
            'lang': 'en_US',
            'post_per_page': '36',
            'print_or_digital': 'digital',
            'post_listing_limit_offset': str(page_no),
            'directory_name': 'latest_pages',
            'template_name': 'lazy_loading',
        }

        return payload
    
    def start_requests(self):     
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse)

    def parse(self, response):

        for index, post in enumerate(response.css(self.selectors['single_post'])):
            
            if not post:  
                self.logger.info("No more posts. Stopping scraper.")
                return

            item = TheNationItem()
            
            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='').strip()
            image_urls = response.css(self.selectors['post_image']).getall()  
            image_url = [re.search(r'url\((.*?)\)', url).group(1) if re.search(r'url\((.*?)\)', url) else '' for url in image_urls]
            item['image_urls'] = [image_url[index]] if image_url and index < len(image_url) else []
            
            yield scrapy.Request(
                url = item['detail_url'],
                callback = self.parse_details,
                meta = {'item': item},
                errback = self.handle_error,
            )

        self.page_counter += 36
        self.logger.info(f"Completed offset {self.page_counter - 36}")
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse,
                                 errback=self.handle_error,)

    def parse_details(self, response):
        item = response.meta['item']
        publication_date = response.css(self.selectors['post_date']).get()
        publication_date = publication_date.split("|")
        item['publication_date'] = publication_date[1].strip()
        item['author'] = response.css(self.selectors['author']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")