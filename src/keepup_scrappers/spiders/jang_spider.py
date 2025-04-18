import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import JangItem

class JangSpider(BaseSpider):
    
    name = 'jang_spider'
    site_key = 'jang'
    
    custom_settings = {
            "IMAGES_STORE": f'data/{site_key}/images/',
            "FEEDS": {
                f"data/{site_key}/data.json": {
                    "format": "json",
                    "encoding": "utf8",
                    "indent": 4,
                }
            },
        
        }
    

    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = self.site_key
        super().__init__(*args, **kwargs)

    def parse(self, response):

        for index, post in enumerate(response.css(self.selectors['single_post'])):

            item = JangItem()
            
            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='').strip()
            image_urls = response.css(self.selectors['post_image']).getall()  
            item['image_urls'] = [image_urls[index]] if image_urls and index < len(image_urls) else []
            item['exerpt']  = post.css(self.selectors['exerpt']).get(default='').strip()
            
            yield scrapy.Request(
                url = item['detail_url'],
                callback = self.parse_details,
                meta = {'item': item},
                errback = self.handle_error,
            )

    def parse_details(self, response):
        item = response.meta['item']
        #item['publication_date'] = response.css(self.selectors['post_date']).extract()[-1].strip()
        dates = response.css(self.selectors['post_date']).extract()
        if dates:  # Check if list is not empty
            item['publication_date'] = dates[-1].strip()
        else:
            item['publication_date'] = "N/A"  # Or handle it as needed
        item['author'] = response.css(self.selectors['author']).get(default='').strip()
        #item['category']  = response.css(self.selectors['category']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")