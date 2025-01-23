from scrapy.crawler import CrawlerProcess
from keepup_scrappers.spiders.sfc_spider import SFCSpider
from keepup_scrappers.spiders.iverify_spider import IverifySpider
from keepup_scrappers.spiders.GFC_spider import GFCSpider
from keepup_scrappers.spiders.fridytimes_spider import FridayTimesSpider
from keepup_scrappers.spiders.geonews_spider import GNSpider
from keepup_scrappers.spiders.snopes_spider import SnopesSpider
from keepup_scrappers.spiders.tribune_spider import tribuneSpider
from keepup_scrappers.spiders.politifact_spider import PolitifactSpider
from scrapy.utils.project import get_project_settings

def run_scrapers():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(IverifySpider)
    process.start()
 
if __name__ == '__main__':
    run_scrapers()