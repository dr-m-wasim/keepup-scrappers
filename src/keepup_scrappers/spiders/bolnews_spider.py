import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import BolNewsItem
import json

class BolNewsSpider(BaseSpider):
    
    name = 'bolnews_spider'
    site_key = 'bolnews'
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
            'ROBOTSTXT_OBEY': False,
        }
    
    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = self.site_key
        super().__init__(*args, **kwargs)

    def get_payload_headers(self, page_no):
        
        payload = {
            'action': 'loadmore',
            'query': '{"category_name":"politics","error":"","m":"","p":0,"post_parent":"","subpost":"","subpost_id":"","attachment":"","attachment_id":0,"name":"","pagename":"","page_id":0,"second":"","minute":"","hour":"","day":0,"monthnum":0,"year":0,"w":0,"tag":"","cat":160461,"tag_id":"","author":"","author_name":"","feed":"","tb":"","paged":0,"meta_key":"","meta_value":"","preview":"","s":"","sentence":"","title":"","fields":"","menu_order":"","embed":"","category__in":[],"category__not_in":[],"category__and":[],"post__in":[],"post__not_in":[],"post_name__in":[],"tag__in":[],"tag__not_in":[],"tag__and":[],"tag_slug__in":[],"tag_slug__and":[],"post_parent__in":[],"post_parent__not_in":[],"author__in":[],"author__not_in":[],"search_columns":[],"ignore_sticky_posts":false,"suppress_filters":false,"cache_results":true,"update_post_term_cache":true,"update_menu_item_cache":false,"lazy_load_term_meta":true,"update_post_meta_cache":true,"post_type":"","posts_per_page":28,"nopaging":false,"comments_per_page":"5","no_found_rows":false,"order":"DESC"}',
            'page': str(page_no),
        }

        return payload
    
    def start_requests(self):     
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 method="POST",
                                 formdata = payload, 
                                 callback = self.parse)


    def parse(self, response):
        posts = response.css(self.selectors['single_post'])
    
        if not posts:
            self.logger.info(f"No posts found on page {self.page_counter}. Stopping pagination.")
            return  # Stop crawling

        for index, post in enumerate(posts):
            item = BolNewsItem()
            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='').strip()
        
            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_details,
                meta={'item': item},
                errback=self.handle_error,
            )

        self.logger.info(f"Page {self.page_counter} completed")
        self.page_counter += 1
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(
            url=self.start_urls[0],
            formdata=payload,
            callback=self.parse,
            errback=self.handle_error,
        )

    def parse_details(self, response):
        item = response.meta['item']
        item['author'] = response.css(self.selectors['author']).get(default='').strip()
        item['publication_date'] = response.css(self.selectors['post_date']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")
        