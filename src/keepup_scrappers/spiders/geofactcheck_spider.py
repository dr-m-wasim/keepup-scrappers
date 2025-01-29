import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import GeofactcheckItem

class GeoFactCheckSpider(BaseSpider):
    
    name = 'geofactcheck_spider'
    page_counter = 1
    site_key = 'geofactcheck'
    
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
            'offset': str(page_no),
            'tag': '0'
        }

        return payload
    
    def start_requests(self):     
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse)

    def parse(self, response):
        if not response.body.strip():
            self.logger.warning("Empty response received.")
            return
        for post in response.css(self.selectors['single_post']):

            item = GeofactcheckItem()

            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            image_url = post.css(self.selectors['post_image']).get(default='')
            item['image_urls'] = [response.urljoin(image_url)] if image_url else []
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='').strip()
            item['publication_date'] = post.css(self.selectors['post_date']).get(default='').strip()

            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_details,
                meta={'item': item},
                errback=self.handle_error,
            )


        self.page_counter += 1
        self.logger.info(f"Completed page {self.page_counter - 1}")
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload, 
                                 callback = self.parse,
                                 errback=self.handle_error)
        

    def parse_details(self, response):
        item = response.meta['item']
        item['author'] = response.xpath(self.selectors['author']).get(default='')
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")