import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import TheNewsItem

class TheNewsSpider(BaseSpider):
    
    name = 'thenews_spider'
    site_key = 'thenews'


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
        self.page_counter = 1

    def parse(self, response):
        categories = ["latest_stories", "business"]
        selectors = next((self.selectors_map.get(cat) for cat in categories if cat in self.selectors_map), None)
            
        for index, post in enumerate(response.css(selectors['single_post'])):

            item = TheNewsItem()
            
            item['title'] = post.css(selectors['post_title']).get(default='').strip()
            item['detail_url'] = post.css(selectors['post_link']).get(default='').strip()
            image_urls = response.css(selectors['post_image']).getall()  
            item['image_urls'] = [image_urls[index]] if image_urls and index < len(image_urls) else []  
            item['exerpt'] = post.css(selectors['exerpt']).get(default='').strip()
            
            
            yield scrapy.Request(
                url = item['detail_url'],
                callback = self.parse_details,
                meta = {'item': item, 'selectors': selectors},
                errback=self.handle_error,
            )

    def parse_details(self, response):
        item = response.meta['item']
        selectors = response.meta.get('selectors', {})
        item['author'] = response.xpath(selectors['author']).get(default='').strip()
        if item['author'] == '':
            item['author'] = response.css(selectors['author2']).get(default='').strip()
        item['publication_date'] = response.css(selectors['post_date']).get(default='').strip()
        content_paragraphs = response.css(selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")