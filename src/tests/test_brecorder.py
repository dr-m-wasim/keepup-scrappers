import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.brecorder_spider import BRecorderSpider

class TestbrecorderSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'brecorder'
        self.spider_name = 'brecorder_spider'
        
        # initialization of spider
        self.spider = BRecorderSpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['brecorder']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        #assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\brecorder\listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 100  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'Pakistan voices alarm over US arms in Afghanistan, links them to cross-border terrorism'
        
        assert item['detail_url'] == 'https://www.brecorder.com/news/40345317/pakistan-voices-alarm-over-us-arms-in-afghanistan-links-them-to-cross-border-terrorism'
        assert item['image_urls'][0] == 'https://i.brecorder.com/medium/2025/01/29222142d5b4215.jpg?r=223417'
        assert item['exerpt'] == 'The Foreign Office (FO) said on Tuesday that the presence of sophisticated American weaponry in Afghanistan, left...'
        assert item['category'] == 'Pakistan'
   
    def test_parse_details_method(self):

        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\brecorder\detail_sample.html', 'r', encoding='utf-8') as f:
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
        assert item['publication_date'] == ''
        assert item['author'] == 'BR Web Desk'
        
        assert item['content'] == "“These weapons have been used by terrorist organisations, including the TTP, to carry out terrorist attacks in Pakistan” the spokesperson asserted. Pakistan’s Foreign Office issued a stern statement while responding to media inquiries about the United States’ move to reclaim advanced military equipment abandoned in Afghanistan. “We have been repeatedly calling upon the de facto authorities in Kabul to take all necessary measures to ensure that these weapons do not fall into the wrong hands,” the statement concluded, reflecting longstanding bilateral tensions over cross-border militancy. Islamabad has persistently urged Afghanistan’s Taliban-led administration to act decisively in securing the abandoned arsenal and preventing its misuse by militants. On the eve of his presidential inauguration, Trump threatened Afghanistan during a public rally, stating that he would cut off all financial assistance if the nation did not return U.S. military equipment, including aircraft, air-to-ground munitions, vehicles, and communication gear. He said, “If we’re going to pay billions of dollars a year, we should tell them that we won’t provide the money unless they return our military equipment.”."