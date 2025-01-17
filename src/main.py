from scrapy.crawler import CrawlerProcess
from keepup_scrappers.settings import BOT_NAME, SPIDER_MODULES
from keepup_scrappers.spiders.sfc_spider import SFCSpider

def run_scrapers():
    process = CrawlerProcess({
        'BOT_NAME': BOT_NAME,
        'SPIDER_MODULES': SPIDER_MODULES,
        'NEWSPIDER_MODULE': SPIDER_MODULES,
        'LOG_LEVEL': 'INFO',
    })
    process.crawl(SFCSpider)
    process.start()

if __name__ == '__main__':
    run_scrapers()