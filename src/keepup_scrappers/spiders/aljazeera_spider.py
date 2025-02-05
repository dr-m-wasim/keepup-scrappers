# import scrapy
# import logging
# from keepup_scrappers.spiders.base_spider import BaseSpider
# from keepup_scrappers.items import AljazeeraItem

# class AljazeeraSpider(BaseSpider):
    
#     name = 'aljazeera_spider'
#     #page_counter = 1
#     site_key = 'aljazeera'
    
#     custom_settings = {
#             "IMAGES_STORE": f'data/{site_key}/images/',
#             "FEEDS": {
#                 f"data/{site_key}/data.json": {
#                     "format": "json",
#                     "encoding": "utf8",
#                     "indent": 4,
#                 }
#             }
#         }

#     def __init__(self, *args, **kwargs):
#         # Pass site_key to the base class
#         kwargs['site_key'] = self.site_key
#         super().__init__(*args, **kwargs)
#         self.offset = 0
        

#     def get_payload_headers(self):
        
#         payload = {
#             'offset': str(self.offset),
           
#         }

#         # Increment the offset for the next call
#         self.offset += 10

#         return payload
    
#     def start_requests(self):     
#         payload = self.get_payload_headers()

#         yield scrapy.FormRequest(url = self.start_urls[0], 
#                                  formdata = payload, 
#                                  callback = self.parse)

#     def parse(self, response):
#         # Check if the response is empty
#         if not response.body.strip():
#             self.logger.warning("Empty response received.")
#             return

#         posts = response.css(self.selectors['single_post'])

#         # If no posts are found, log completion and stop further scraping
#         if not posts:
#             self.logger.info(f"Offset {self.offset}: No new posts available. Scraping complete.")
#             return

#         # Process each post found in the response
#         for post in posts:
#             item = AljazeeraItem()

#             item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
#             item['detail_url'] = post.css(self.selectors['post_link']).get(default='').strip()
#             item['publication_date'] = post.css(self.selectors['post_date']).get(default='').strip()
#             item['label'] = post.css(self.selectors['label']).get(default='').strip()
#             exerpt = post.css(self.selectors['excerpt']).get(default='').strip()

#             # Request the detail page for each post
#             yield scrapy.Request(
#                 url=item['detail_url'],
#                 callback=self.parse_details,
#                 meta={'item': item},
#                 errback=self.handle_error,
#             )

#         # Get payload headers for the next page
#         payload = self.get_payload_headers(self.page_counter)
#         yield scrapy.FormRequest(
#             url=self.start_urls[0], 
#             formdata=payload, 
#             callback=self.parse,
#             errback=self.handle_error
#         )

        

#     def parse_details(self, response):
#         item = response.meta['item']
        
#         content_paragraphs = response.css(self.selectors['content']).getall()
#         item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

#         yield item

#     def handle_error(self, failure):
#         self.logger.error(f"Request Failed: {failure.request.url}")

import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import AljazeeraItem

class AljazeeraSpider(BaseSpider):
    
    name = 'aljazeera_spider'

    site_key = 'aljazeera'
    #page_counter = 1
    
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

    
    def parse(self, response):
       
        for post in response.css(self.selectors['single_post']):
            
            item = AljazeeraItem()

            item['title'] = post.css(self.selectors['post_title']).get(default='').strip() 
            relative_url = post.css(self.selectors['post_link']).get(default='')
            item['detail_url'] = response.urljoin(relative_url) if relative_url else []
            item['publication_date'] = post.css(self.selectors['post_date']).get(default='').strip()
            item['exerpt'] = post.css(self.selectors['exerpt']).get(default='').strip()


            if item['detail_url']:
                # Combine relative URL with base URL using response.urljoin
                full_url = response.urljoin(item['detail_url'])
                
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_details,
                    meta={'item': item},
                    errback=self.handle_error,
                )


    def parse_details(self, response):
        item = response.meta['item']
        
        item['content'] = ' '.join(response.css(self.selectors['content']).getall()).strip()
        
       

        yield item
    
    
    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")