import scrapy
from datetime import datetime, timedelta
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import DawnnewsItem

class DawnSpider(BaseSpider):
    name = 'dawn_spider'
    site_key = 'dawn'

    custom_settings = {
        "IMAGES_STORE": f"data/{site_key}/images/",
        "FEEDS": {
            f"data/{name}/data.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
            }
        },
        "DOWNLOAD_DELAY": 3,
    }

    def __init__(self, *args, **kwargs):
        kwargs['site_key'] = self.site_key
        super().__init__(*args, **kwargs)

        if not self.selectors:
            raise ValueError(f"Selectors configuration for site '{self.site_key}' not found.")

        self.current_date = datetime.today()
        
        self.start_urls = [f"https://www.dawn.com/latest-news/{self.current_date.strftime('%Y-%m-%d')}"]

        
    def parse(self, response):
        posts = response.css(self.selectors['single_post'])
        
        if not posts:
            self.logger.info(f"No posts found for {self.current_date.strftime('%Y-%m-%d')}. Stopping the spider.")
            return  # Stop moving backward if no posts

        for post in posts:
            item = DawnnewsItem()
            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='').strip()
            item['detail_url'] = response.urljoin(item['detail_url'])

            if item['detail_url']:
                yield scrapy.Request(
                    url=item['detail_url'],
                    callback=self.parse_details,
                    meta={'item': item},
                    errback=self.handle_error,
                )

        self.logger.info(f"Scraped data for {self.current_date.strftime('%Y-%m-%d')}")

        # Move to the previous day
        self.current_date -= timedelta(days=1)

        # STOP if we cross the last date
        if self.current_date < datetime(2013, 1, 1):
            self.logger.info("Reached the cutoff date. Stopping the spider.")
            return

        # Else continue
        formatted_date = self.current_date.strftime("%Y-%m-%d")
        next_url = self.base_url.format(date=formatted_date)

        yield scrapy.Request(
            url=next_url,
            callback=self.parse,
            errback=self.handle_error,
        )

    def parse_details(self, response):
        item = response.meta['item']
        item['author'] = response.css(self.selectors['author']).get(default='').strip()
        item['content'] = ' '.join(response.css(self.selectors['content']).getall() or []).strip()
        item['publication_date'] = response.css(self.selectors['post_date']).get()

        yield item


    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")
        if failure.check(scrapy.spidermiddlewares.httperror.HttpError):
            response = failure.value.response
            self.logger.error(f"HTTP Error {response.status} for {failure.request.url}")
        else:
            self.logger.error(f"Error Details: {failure.value}")

