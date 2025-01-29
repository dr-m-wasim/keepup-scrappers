from scrapy.crawler import CrawlerProcess
from keepup_scrappers.spiders.pakiverify_spider import PakIverifySpider
from keepup_scrappers.spiders.factcheckorg_spider import FactcheckorgSpider
from scrapy.utils.project import get_project_settings

def run_scrapers():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(FactcheckorgSpider)
    process.start()
 
if __name__ == '__main__':
    run_scrapers()