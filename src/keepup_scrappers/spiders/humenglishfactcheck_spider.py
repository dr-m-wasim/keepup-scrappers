import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import HumEnglishFactcheckItem

class HumEnglishFactcheckSpider(BaseSpider):
    
    name = 'humenglishfactcheck_spider'
    site_key = 'humenglishfactcheck'
    
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

        for index, post in enumerate(response.css(self.selectors['single_post'])):
            item = HumEnglishFactcheckItem()

            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='').strip()
            #image_urls = response.css(self.selectors['post_image']).getall()  
            #item['image_urls'] = [image_urls[index]] if image_urls and index < len(image_urls) else []
            item['publication_date'] = post.css(self.selectors['post_date']).get(default='').strip()
            exerpt = post.css(self.selectors['exerpt']).getall()
            item['exerpt'] = exerpt[1] if len(exerpt) > 1 else " "
            
            yield scrapy.Request(
                url = item['detail_url'],
                callback = self.parse_details,
                meta = {'item': item},
                errback = self.handle_error,
            )

        self.logger.info(f"Page {self.page_counter} completed")
        
        self.page_counter += 1
        next_page = response.css(self.selectors['next_page']).get(default='').strip()  
        
        if next_page:
            yield scrapy.Request(
                url =  next_page,
                callback = self.parse,
                errback = self.handle_error,
            )
    
    def parse_details(self, response):
        item = response.meta['item']
        item['label'] = response.xpath(self.selectors['label']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")