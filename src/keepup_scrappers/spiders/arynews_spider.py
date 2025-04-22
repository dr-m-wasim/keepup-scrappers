import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import AryNewsItem
import re
import json

class AryNewsSpider(BaseSpider):
    
    name = 'arynews_spider'
    site_key = 'arynews'
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
            "DOWNLOAD_DELAY": 2,
            'ROBOTSTXT_OBEY': False,
        }
    
    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = self.site_key
        super().__init__(*args, **kwargs)

    
    def parse(self, response):

        for index, post in enumerate(response.css(self.selectors['single_post'])):

            if not post:  
                self.logger.info("No more posts. Stopping scraper.")
                return
            item = AryNewsItem()
            
            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='').strip()
            image_url = post.css(self.selectors['post_image']).get(default='')
            image_url = re.search(r'url\((.*?)\)', image_url).group(1)
            #item['image_urls'] = [response.urljoin(image_url)] if image_url else []
            
            yield scrapy.Request(
                url = item['detail_url'],
                callback = self.parse_details,
                meta = {'item': item},
                errback = self.handle_error,
            )

        self.logger.info(f"Page {self.page_counter} completed")
        self.page_counter += 1

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 callback = self.parse,
                                 errback=self.handle_error,)

    def parse_details(self, response):
        item = response.meta['item']
        item['publication_date'] = response.css(self.selectors['post_date']).get(default='')
        item['author'] = response.css(self.selectors['author']).get(default='').strip()
        item['exerpt']  = response.css(self.selectors['exerpt']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")