import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.jang_spider import JangSpider

class TestjangSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'jang'
        self.spider_name = 'jang_spider'
        
        # initialization of spider
        self.spider = JangSpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['jang']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        #assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\jang\listing_sample (2).html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 30 # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == "Netflix takes big step against ‘Emilia Pérez’ star Karla Sofía Gascón"
        assert item['image_urls'][0] == 'https://jang.com.pk/assets/uploads/english_news/2025-02-05/b_31007_065616_eng.jpg'
        assert item['detail_url'] == 'https://jang.com.pk/en/31007-netflix-takes-big-step-against-emilia-prez-star-karla-sofa-gascn-news'
        assert item['exerpt'] == 'Karla Sofía Gascón faces Netflix setback amid Oscar controversy'
        
        #assert item['author'] == 'CEJ'
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\jang\detail_sample (3).html', 'r', encoding='utf-8') as f:
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
        assert item['content'] == "Netflix has taken a major step against star Karla Sofía Gascón after her “racist” tweets resurfaced on the internet. The Oscar-nominated actor also was asked to withdraw from the nomination. As per Netflix has reportedly removed Karla from promotional emails. The media giant seemingly plans to remove her from poster and give Zoe Saldana more prominence. Karla, 52, got nominated for Best Actress at the Academy Awards, for her role as a transgender crime boss in the hit film. She recently told , “I cannot step down from an Oscar nomination because I have not committed any crime nor have I harmed anyone. I am neither racist nor anything that all these people have tried to make others believe I am.” The Spanish starlet landed in hot water last week after netizens found out her racist remarks about George Floyd in 2020. “I have been judged, condemned, sacrificed, crucified, and stoned without a trial and without the option to defend myself,” Karla noted. She also received backlash for her anti-Islamic tweets. Notably, she has been nominated for an Oscar Award for best actress for her role in"
        
        assert item['publication_date'] == 'February 05, 2025'
        assert item['author'] == 'Web Desk'
        assert item['category'] == 'Entertainment'