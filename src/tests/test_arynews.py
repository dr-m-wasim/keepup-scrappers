import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.arynews_spider import AryNewsSpider

class TestArynewsSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'arynews'
        self.spider_name = 'arynews_spider'
        
        
        # initialization of spider
        self.spider = AryNewsSpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['arynews']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        #assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\arynews\listing_sample (2).html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 9  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'Govt has nothing to offer in talks, says Omar Ayub'
        
        assert item['detail_url'] == 'https://arynews.tv/govt-nothing-offer-in-talks-omar-ayub/'
        assert item['image_urls'][0] == 'https://arynews.tv/wp-content/uploads/2024/12/omar-ayub.jpg'
         
        
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\arynews\detail_sample (3).html', 'r', encoding='utf-8') as f:
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
        assert item['author'] == 'Web Desk'
        assert item['exerpt'] == 'ISLAMABAD: Opposition leader in the National Assembly Omar Ayub on Monday said that the PTI will observe black day in Swabi on February 08, ARY News reported.'
        assert item['publication_date'] == 'Monday, February 3, 2025'
        assert item['content'] == "PTI leader talking to media here said that the government has nothing in its hands to offer during the talks. Omar Ayub said that the situation has been worsened in Balochistan. He claimed that Prime Minister Shehbaz Sharif has no courage to speak in the National Assembly. A dialogue between the government and opposition PTI, for the sake of political stability in the country, was reached to a stalemate after the PTI decided not to attend the fourth round of the talks owing to the government’s no reply over the opposition party’s demand for constitution of a judicial commission. Chairman PTI Barrister Gohar Ali said that the party will not attend the 4th round of dialogue. Talking to media he said that the government was given seven days’ deadline, but it has still not announced the judicial commission. However, the National Assembly Speaker Ayaz Sadiq who was presiding over the dialogue said that the government’s negotiating committee will continue its efforts to engage in dialogue with the opposition, despite the opposition’s absence from the talks."