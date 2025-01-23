from scrapy.crawler import CrawlerProcess
from keepup_scrappers.settings import BOT_NAME, SPIDER_MODULES
from keepup_scrappers.spiders.sfc_spider import SFCSpider
from keepup_scrappers.spiders.iverify_spider import IverifySpider
from keepup_scrappers.spiders.GFC_spider import GFCSpider
from keepup_scrappers.spiders.fridytimes_spider import FridayTimesSpider
from keepup_scrappers.spiders.geonews_spider import GNSpider
from keepup_scrappers.spiders.snopes_spider import SnopesSpider
from keepup_scrappers.spiders.tribune_spider import tribuneSpider
from keepup_scrappers.spiders.politifact_spider import PolitifactSpider

def run_scrapers():
    process = CrawlerProcess({
        'BOT_NAME': BOT_NAME,
        'SPIDER_MODULES': SPIDER_MODULES,
        'NEWSPIDER_MODULE': SPIDER_MODULES,
        'LOG_LEVEL': 'INFO',
    })
    #process.crawl(SFCSpider)
    #process.crawl(IverifySpider)
    #process.crawl(GFCSpider)

    #process.crawl(GNSpider)
    process.crawl(tribuneSpider)

    #process.crawl(FridayTimesSpider)
    #process.crawl(SnopesSpider)
    process.crawl(PolitifactSpider)
    process.crawl(SnopesSpider)

    process.start()

if __name__ == '__main__':
    run_scrapers()