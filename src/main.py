from scrapy.crawler import CrawlerProcess
from keepup_scrappers.spiders.pakiverify_spider import PakIverifySpider
from keepup_scrappers.spiders.dailytimes_spider import DailyTimesSpider
from scrapy.utils.project import get_project_settings

def run_scrapers():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(DailyTimesSpider)
    process.start()
 
if __name__ == '__main__':
    run_scrapers()