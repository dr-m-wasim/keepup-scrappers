import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.thefridaytimesfactcheck_spider import FridayTimesSpider

class TestthefridaytimesfactcheckSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'thefridaytimesfactcheck'
        self.spider_name = 'thefridaytimesfactcheck_spider'
        
        # initialization of spider
        self.spider = FridayTimesSpider()
        
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['thefridaytimesfactcheck']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 0
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\thefridaytimesfactcheck\listing_sample (1).html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 21  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'Fact-Check: Is Punjab CM Maryam Nawaz Suffering From Throat Cancer?'
        
        assert item['detail_url'] == 'https://thefridaytimes.com/14-Nov-2024/fact-check-is-punjab-cm-maryam-nawaz-suffering-from-throat-cancer'
        assert item['image_urls'][0] == 'https://thefridaytimes.com/digital_images/medium/2024-11-14/fact-check-is-punjab-cm-maryam-nawaz-suffering-from-throat-cancer-1731576412-8524.jpg'
        
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\thefridaytimesfactcheck\detail_sample (1).html', 'r', encoding='utf-8') as f:
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
        assert item['publication_date'] == ' November 14, 2024 '
        assert item['content'] == "Punjab Chief Minister Maryam Nawaz’s recent visit to Geneva sparked widespread speculation on social media after journalist Mansoor Ali Khan claimed that her trip was not for routine treatment, but due to a cancer diagnosis. However, the air has now been cleared, as CM Maryam Nawaz has denied the media reports suggesting she has throat cancer. Speaking at a Pakistan Muslim League-Nawaz (PML-N) event in London, Maryam explained that her health issues are related to her parathyroid gland, not cancer. She was joined by her father, former Prime Minister Nawaz Sharif, at the event organized by PML-N UK President Ahsan Dar. Maryam confirmed that she had recently visited Geneva for medical check-ups and assured her supporters that the cancer rumors were false. She explained that her condition, which involves the parathyroid gland, can only be treated in Switzerland or the United States. “I’ve been working non-stop for eight months and suffering from this condition. I want to make it clear that I do not have throat cancer,” she said. Maryam also noted that she did not want to draw attention to her health but felt compelled to address the rumors. She added that she would return to Pakistan in two days, putting an end to the speculation about her health."