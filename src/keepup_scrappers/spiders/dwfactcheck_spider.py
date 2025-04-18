import scrapy
import time
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import DWfactcheckItem

class DWfactcheckSpider(BaseSpider):
    
    name = 'dwfactcheck_spider'
    site_key = 'dwfactcheck'
    page_counter = 2
    
    custom_settings = {
            # Scrapy Playwright settings
            "PLAYWRIGHT_BROWSER_TYPE": "chromium",
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
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
        self.page_counter = 2

    def start_requests(self):     
        yield scrapy.Request(
            url= self.start_urls[0],
            meta={"playwright": True},
            callback = self.parse,
        )

    def parse(self, response):
        time.sleep(10)
        for post in response.css(self.selectors['single_post']):
            item = DWfactcheckItem()
            item['title'] = post.css(self.selectors['post_title']).get(default='')
            #image_urls = response.css(self.selectors['post_image']).getall()
            #item['image_urls'] = [response.urljoin(image_urls[0])] if image_urls else []
            relative_url = post.css(self.selectors['post_link']).get(default='')
            item['detail_url'] = response.urljoin(relative_url) if relative_url else [] 
            item['publication_date'] = post.css(self.selectors['post_date']).get(default='')
            item['category'] = post.css(self.selectors['category']).get(default='')
            item['exerpt'] = post.css(self.selectors['exerpt']).get(default='')

            if item['detail_url']:
                yield scrapy.Request(
                    url=item['detail_url'],
                    callback=self.parse_details,
                    meta={'item': item},
                    errback=self.handle_error,
                )

        self.logger.info(f"Page {self.page_counter} completed")
        self.page_counter += 1
        get_next_page = response.css(self.selectors['next_page']).get()
        next_page = response.urljoin(get_next_page) 
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse,
                errback=self.handle_error,
            )

    def parse_details(self, response):
        item = response.meta['item']
        item['author'] = response.css(self.selectors['author']).get(default='')
        item['label'] = response.xpath(self.selectors['label']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")