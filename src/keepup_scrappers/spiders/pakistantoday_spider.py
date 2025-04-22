import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import PakistanTodayItem
import json
from scrapy.selector import Selector

class PakistanTodaySpider(BaseSpider):
    
    name = 'pakistantoday_spider'
    site_key = 'pakistantoday'
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
            'ROBOTSTXT_OBEY': False,
            #'DOWNLOAD_DELAY': 1
        }
        
    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = self.site_key
        super().__init__(*args, **kwargs)

    def get_payload_headers(self, page_no):
        
        payload = {
            "action": "td_ajax_loop",
            "loopState[sidebarPosition]": "", 
            "loopState[moduleId]": "10",
            "loopState[currentPage]": str(page_no),
            "loopState[max_num_pages]": "2643",
            "loopState[atts][category_id]": "23266",
            "loopState[ajax_pagination_infinite_stop]": "0",
            "loopState[server_reply_html_data]": ""
        }

        return payload
    
    def start_requests(self):     
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        html_content = data.get("server_reply_html_data", "")
        html_selector = Selector(text=html_content)

        for post in html_selector.css(self.selectors['single_post']):

            item = PakistanTodayItem()

            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='') 
            #image_urls = post.css(self.selectors['post_image']).getall()
            #item['image_urls'] = image_urls if image_urls else []
            item['exerpt']  = post.css(self.selectors['exerpt']).get(default='').strip()

            
            yield scrapy.Request(
                url = item['detail_url'],
                callback = self.parse_details,
                meta = {'item': item},
                errback = self.handle_error,
            )

        self.logger.info(f"Completed Page {self.page_counter}")
        self.page_counter += 1
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse,
                                 errback=self.handle_error,)


    def parse_details(self, response):
        item = response.meta['item']
        item['author'] = response.css(self.selectors['author']).get(default='').strip()
        item['publication_date'] = response.css(self.selectors['post_date']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")