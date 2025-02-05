import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.aljazeera_spider import AljazeeraSpider

class TestaljazeeraSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'aljazeera'
        self.spider_name = 'aljazeera_spider'
        
        # initialization of spider
        self.spider = AljazeeraSpider()
        
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['aljazeera']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        #assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\aljazeera\listing_sample (2).html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 13  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'Cummins ‘hugely unlikely’ for Australia’s ICC Champions Trophy bid'
        
        assert item['detail_url'] == 'https://www.aljazeera.com/sports/2025/2/5/injured-cummins-set-to-miss-australias-icc-champions-trophy-bid'
        assert item['publication_date'] == 'Published On 5 Feb 2025'
        
        
        assert item['exerpt'] == 'Australia captain Pat Cummins doubtful to lead his team at the ICC event in Pakistan due to injury, personal reasons.'
   
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
        
        assert item['content'] == ""