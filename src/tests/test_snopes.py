import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.snopes_spider import SnopesSpider

class TestIverifySpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'snopes'
        self.spider_name = 'snopes_spider'
        
        # initialization of spider
        self.spider = SnopesSpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['snopes']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'E:\keepup\keepup-scrappers\src\tests\test_data\snopes\listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 21  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'No, Trump Did Not Sign Executive Order Ending Food Stamps, Cash Assistance'
        assert item['publication_date'] == 'Jan. 28, 2025'
        assert item['detail_url'] == 'https://www.snopes.com/fact-check/trump-eo-ending-food-stamps/'
        assert item['image_urls'][0] == 'https://mediaproxy.snopes.com/width/600/https://media.snopes.com/2025/01/food_stamps_satire.jpg'
         
        assert item['author'] == 'Taija PerryCook'
   
    def test_parse_details_method(self):

        with open(r'E:\keepup\keepup-scrappers\src\tests\test_data\snopes\detail_sample.html', 'r', encoding='utf-8') as f:
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
        assert item['label'] == 'False'
        assert item['content'] == "On Jan. 27, 2025, a claim that U.S. President signed an executive order to end food stamps and federal cash assistance made its rounds on the internet. , which gained more than 215,500 views as of this writing, featured a video of someone saying: TikTok user @krystalsohipapate first on Jan. 25, 2025, and that post received more than 2.2 million views and 50,200 likes, as of this writing. Users flooded both posts with comments that indicated they believed the claim that Trump signed such an executive order. However, out of the Trump signed in the first days of his second presidential term, there was no evidence any of them ended federal food stamps or cash assistance programs. The X account that posted the video said \" \" in its bio, While as to whether Trump allies want to make cuts to the federal food stamp program, we have not substantiated these claims. The specific claim in this video, however that Trump signed an executive order to end food stamps and cash assistance is false. For background, here is we alert readers to rumors created by sources that call their output humorous or satirical."