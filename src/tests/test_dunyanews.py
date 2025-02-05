import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.dunyanews_spider import DunyaNewsSpider

class TestduniyanewsSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'dunyanews'
        self.spider_name = 'dunyanews_spider'
        
        # initialization of spider
        self.spider = DunyaNewsSpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['dunyanews']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        #assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\dunyanews\listing_sample (2).html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 32 # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == "KP stands with Kashmir in their struggle for freedom, says Gandapur"
        assert item['image_urls'][0] == 'https://img.dunyanews.tv/news/2025/February/02-05-25/news_big_images/866514_60434377.jpg'
        assert item['detail_url'] == 'https://dunyanews.tv/index.php/en/Pakistan/866514-kp-stands-with-kashmir-in-their-struggle-for-freedom-says-gandapur'
        
        
        #assert item['author'] == 'CEJ'
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\dunyanews\detail_sample (2).html', 'r', encoding='utf-8') as f:
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
        assert item['content'] == "Pakistan KP stands with Kashmir in their struggle for freedom, says Gandapur Gandapur emphasised that both the people & govt of KP stand in complete solidarity with Kashmir PESHAWAR (Dunya News) – On the occasion of Kashmir Solidarity Day, Khyber Pakhtunkhwa Chief Minister Ali Amin Gandapur reaffirmed the province's unwavering support for the Kashmiri people's struggle for freedom. In his message, Gandapur emphasised that both the people and government of Khyber Pakhtunkhwa stand in complete solidarity with Kashmir. He asserted that the right to freedom is a fundamental right of the Kashmiri people, and Pakistan remains committed to supporting them morally, diplomatically, and politically. He urged international human rights organisations to take notice of the ongoing atrocities committed by Indian forces in occupied Kashmir, highlighting that regional peace is intrinsically linked to the resolution of the Kashmir issue. \"The establishment of lasting peace in the region is impossible without addressing the Kashmir conflict,\" Gandapur stated. \"India continues to deploy new tactics to suppress the Kashmiri freedom movement, but the resilience of the Kashmiri people remains unshaken.\""

        assert item['publication_date'] == 'Wed, 05 Feb 2025'
        