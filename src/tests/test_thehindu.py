import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.thehindu_spider import ThehinduSpider

class TestTribuneSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'thehindu'
        self.spider_name = 'thehindu_spider'
        
        # initialization of spider
        self.spider = ThehinduSpider()
        
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['thehindu']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\thehindu\listing_sample (1).html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 15  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'Philippine President offers a deal to China, says will return U.S. missile system'
        assert item['author'] == ' AP'
        assert item['image_urls'][0] == 'https://th-i.thgim.com/public/incoming/2ednti/article69161000.ece/alternates/SQUARE_80/Philippines-China-US_Missiles_18435.jpg'
        assert item['detail_url'] == 'https://www.thehindu.com/news/international/philippine-president-offers-a-deal-to-china-says-will-return-us-missile-system/article69159898.ece'
        
        
        #assert item['author'] == 'CEJ'
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\thehindu\detail_sample (1).html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # example URL
        sample_url = "http://www.example.com/"
        request = Request(url = sample_url, meta = { 'item' : {}} )
        
        mock_response = HtmlResponse(
            url = sample_url,
            request = request,
            body = html_content,
            encoding = 'utf-8'
        )

        results = list(self.spider.parse_details(mock_response))
        assert len(results) == 1
        
        item = results[0]
        assert item['exerpt'] == 'Officials say Dubai International Airport saw a record 92.3 million passengers pass through its terminals in 2024'

        assert item['publication_date'] == '- January 30, 2025 09:23 pm IST - DUBAI'
        