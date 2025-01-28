from scrapy.crawler import CrawlerProcess
from keepup_scrappers.spiders.iverify_spider import IverifySpider
from keepup_scrappers.spiders.GFC_spider import GFCSpider
from scrapy.utils.project import get_project_settings

def run_scrapers():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(GFCSpider)
    process.start()
 
if __name__ == '__main__':
    run_scrapers()