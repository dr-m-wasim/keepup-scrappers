from scrapy.crawler import CrawlerProcess
from keepup_scrappers.spiders.iverify_spider import IverifySpider
from scrapy.utils.project import get_project_settings

def run_scrapers():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(IverifySpider)
    process.start()
 
if __name__ == '__main__':
    run_scrapers()